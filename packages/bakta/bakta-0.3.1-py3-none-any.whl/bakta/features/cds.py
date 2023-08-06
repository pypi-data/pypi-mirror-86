
import logging
import subprocess as sp
from collections import OrderedDict
from typing import Sequence

from Bio import SeqIO

import bakta.config as cfg
import bakta.constants as bc
import bakta.utils as bu
import bakta.so as so
import bakta.io.fasta as fasta

log = logging.getLogger('CDS')


def predict(genome, sequences_path):
    """Predict open reading frames with Prodigal."""

    # create prodigal trainining file if not provided by the user
    prodigal_tf_path = cfg.prodigal_tf
    if(prodigal_tf_path is None):
        if(genome['size'] >= 20000):
            prodigal_tf_path = cfg.tmp_path.joinpath('prodigal.tf')
            log.info('create prodigal training file: file=%s', prodigal_tf_path)
            execute_prodigal(genome, sequences_path, prodigal_tf_path, train=True, complete=genome['complete'])
        else:
            log.info('skip creation of prodigal training file: genome-size=%i', genome['size'])
    else:
        log.info('use provided prodigal training file: file=%s', prodigal_tf_path)

    sequences = {k['id']: k for k in genome['contigs']}
    cdss = []

    # execute prodigal for non-complete sequences (contigs)
    contigs_path = cfg.tmp_path.joinpath('contigs.fasta')
    contigs = [c for c in genome['contigs'] if not c['complete']]
    if(len(contigs) > 0):
        fasta.export_contigs(contigs, contigs_path)
        log.debug('export contigs: # contigs=%i, path=%s', len(contigs), contigs_path)
        proteins_contigs_path = cfg.tmp_path.joinpath('prodigal.proteins.contigs.faa')
        gff_contigs_path = cfg.tmp_path.joinpath('prodigal.contigs.gff')
        log.info('run prodigal: type=contigs, # sequences=%i', len(contigs))
        execute_prodigal(genome, contigs_path, prodigal_tf_path, proteins_path=proteins_contigs_path, gff_path=gff_contigs_path, complete=False)
        cds = parse_prodigal_output(genome, sequences, gff_contigs_path, proteins_contigs_path)
        log.info('contig cds: predicted=%i', len(cds))
        cdss.extend(cds)
    
    # execute prodigal for complete replicons (chromosomes/plasmids)
    replicons_path = cfg.tmp_path.joinpath('replicons.fasta')
    replicons = [c for c in genome['contigs'] if c['complete']]
    if(len(replicons) > 0):
        fasta.export_contigs(replicons, replicons_path)
        log.debug('export replicons: # contigs=%i, path=%s', len(replicons), replicons_path)
        proteins_replicons_path = cfg.tmp_path.joinpath('prodigal.proteins.replicons.faa')
        gff_replicons_path = cfg.tmp_path.joinpath('prodigal.replicons.gff')
        log.info('run prodigal: type=replicons, # sequences=%i', len(replicons))
        execute_prodigal(genome, replicons_path, prodigal_tf_path, proteins_path=proteins_replicons_path, gff_path=gff_replicons_path, complete=True)
        cds = parse_prodigal_output(genome, sequences, gff_replicons_path, proteins_replicons_path)
        log.info('replicon cds: predicted=%i', len(cds))
        cdss.extend(cds)
    
    log.info('predicted=%i', len(cdss))
    return cdss


def execute_prodigal(genome, contigs_path, traininng_file_path, proteins_path=None, gff_path=None, train=False, complete=False):
    log.debug('execute-prodigal: contigs-path=%s, traininng-file-path=%s, proteins-path=%s, gff-path=%s, train=%s, complete=%s', contigs_path, traininng_file_path, proteins_path, gff_path, train, complete)
    cmd = [
        'prodigal',
        '-i', str(contigs_path),
        '-g', str(cfg.translation_table)  # set translation table
    ]
    if(not complete):
        cmd.append('-c')  # closed ends
    if(train):
        cmd.append('-t')
        cmd.append(str(traininng_file_path))
    else:
        if(genome['size'] < 20000):  # no trainings file provided and not enough sequence information available
            cmd.append('-p')  # run prodigal in meta mode
            cmd.append('meta')
        elif(traininng_file_path):
            cmd.append('-t')
            cmd.append(str(traininng_file_path))
        if(proteins_path):  # aa fasta output
            cmd.append('-a')
            cmd.append(str(proteins_path))
        if(gff_path):  # GFF output
            cmd.append('-f')
            cmd.append('gff')
            cmd.append('-o')
            cmd.append(str(gff_path))

    log.debug('cmd=%s', cmd)
    proc = sp.run(
        cmd,
        cwd=str(cfg.tmp_path),
        env=cfg.env,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        universal_newlines=True
    )
    if(proc.returncode != 0):
        log.debug('stdout=\'%s\', stderr=\'%s\'', proc.stdout, proc.stderr)
        log.warning('ORFs failed! prodigal-error-code=%d', proc.returncode)
        raise Exception(f'prodigal error! error code: {proc.returncode}')


def parse_prodigal_output(genome, sequences, gff_path, proteins_path):
    log.debug('parse-prodigal-output: gff-path=%s, proteins-path=%s', gff_path, proteins_path)
    # parse orfs
    # TODO: replace code by BioPython GFF3 parser
    cdss = {}
    partial_cdss_per_record = {}
    partial_cdss_per_contig = {k['id']: [] for k in genome['contigs']}
    with gff_path.open() as fh:
        for line in fh:
            if(line[0] != '#'):
                (contig_id, inference, _, start, stop, score, strand, _, annotations_raw) = line.strip().split('\t')
                gff_annotations = split_gff_annotation(annotations_raw)
                contig_orf_id = gff_annotations['ID'].split('_')[1]

                cds = OrderedDict()
                cds['type'] = bc.FEATURE_CDS
                cds['contig'] = contig_id
                cds['start'] = int(start)
                cds['stop'] = int(stop)
                cds['strand'] = bc.STRAND_FORWARD if strand == '+' else bc.STRAND_REVERSE
                cds['gene'] = None
                cds['product'] = None
                cds['start_type'] = gff_annotations['start_type']
                cds['rbs_motif'] = gff_annotations['rbs_motif']
                cds['db_xrefs'] = [so.SO_CDS.id]
                
                if(cds['strand'] == bc.STRAND_FORWARD):
                    cds['frame'] = (cds['start'] - 1) % 3 + 1
                else:
                    cds['frame'] = (sequences[cds['contig']]['length'] - cds['stop']) % 3 + 1
                
                if(gff_annotations['partial'] == '10'):
                    cds['truncated'] = bc.FEATURE_END_5_PRIME if cds['strand'] == bc.STRAND_FORWARD else bc.FEATURE_END_3_PRIME
                    partial_cdss_per_record[f"{cds['contig']}_{contig_orf_id}"] = cds
                    partial_cdss_per_contig[cds['contig']].append(cds)
                elif(gff_annotations['partial'] == '01'):
                    cds['truncated'] = bc.FEATURE_END_3_PRIME if cds['strand'] == bc.STRAND_FORWARD else bc.FEATURE_END_5_PRIME
                    partial_cdss_per_record[f"{cds['contig']}_{contig_orf_id}"] = cds
                    partial_cdss_per_contig[cds['contig']].append(cds)
                else:
                    cdss[f"{cds['contig']}_{contig_orf_id}"] = cds
                
                log.info(
                    'contig=%s, start=%i, stop=%i, strand=%s, frame=%s, truncated=%s, start-type=%s, RBS-motif=%s',
                    cds['contig'], cds['start'], cds['stop'], cds['strand'], cds['frame'], cds.get('truncated', 'no'), cds['start_type'], cds['rbs_motif']
                )

    # extract translated orf sequences
    with proteins_path.open() as fh:
        for record in SeqIO.parse(fh, 'fasta'):
            cds = cdss.get(record.id, None)
            if(cds):
                seq = str(record.seq)[:-1]  # discard trailing asterisk
                cds['sequence'] = seq
                cds['aa_digest'], cds['aa_hexdigest'] = bu.calc_aa_hash(seq)
            else:
                partial_cds = partial_cdss_per_record.get(record.id, None)
                if(partial_cds):
                    seq = str(record.seq)
                    partial_cds['sequence'] = seq
                    partial_cds['aa_digest'], partial_cds['aa_hexdigest'] = bu.calc_aa_hash(seq)
    cdss = list(cdss.values())

    # merge matching partial features on sequence edges
    for partial_cdss in partial_cdss_per_contig.values():
        if(len(partial_cdss) >= 2):  # skip unpaired edge features
            first_partial_cds = partial_cdss[0]  # first partial CDS per contig
            last_partial_cds = partial_cdss[-1]  # last partial CDS per contig
            # check if partial CDS are on same strand
            # and have opposite truncated edges
            # and firtst starts at 1
            # and last ends at contig end (length)
            if(first_partial_cds['strand'] == last_partial_cds['strand']
                and first_partial_cds['truncated'] != last_partial_cds['truncated']
                and first_partial_cds['start'] == 1
                and last_partial_cds['stop'] == sequences[last_partial_cds['contig']]['length']
                and sequences[first_partial_cds['contig']]['topology'] == bc.TOPOLOGY_CIRCULAR):
                cds = last_partial_cds
                cds['stop'] = first_partial_cds['stop']
                if(last_partial_cds['truncated'] == bc.FEATURE_END_3_PRIME):
                    seq = last_partial_cds['sequence'] + first_partial_cds['sequence']  # merge sequence
                else:
                    seq = first_partial_cds['sequence'] + last_partial_cds['sequence']  # merge sequence
                    cds['start_type'] = first_partial_cds['start_type']
                    cds['rbs_motif'] = first_partial_cds['rbs_motif']
                log.debug(f'trunc seq: seq-start={seq[:10]}, seq-end={seq[-10:]}')

                cds['edge'] = True  # mark CDS as edge feature
                cds.pop('truncated')

                seq = seq[:-1]  # discard trailing asterisk
                cds['sequence'] = seq
                cds['aa_digest'], cds['aa_hexdigest'] = bu.calc_aa_hash(seq)
                cdss.append(cds)
                log.info(
                    'edge CDS: contig=%s, start=%i, stop=%i, strand=%s, frame=%s, start-type=%s, RBS-motif=%s, aa-hexdigest=%s, seq=[%s..%s]',
                    cds['contig'], cds['start'], cds['stop'], cds['strand'], cds['frame'], cds['start_type'], cds['rbs_motif'], cds['aa_hexdigest'], seq[:10], seq[-10:]
                )
                partial_cdss = partial_cdss[1:-1]
        for partial_cds in partial_cdss:
            cdss.append(partial_cds)
            log.info(
                'truncated CDS: contig=%s, start=%i, stop=%i, strand=%s, frame=%s, truncated=%s, start-type=%s, RBS-motif=%s, aa-hexdigest=%s, seq=[%s..%s]',
                partial_cds['contig'], partial_cds['start'], partial_cds['stop'], partial_cds['strand'], partial_cds['frame'], partial_cds['truncated'], partial_cds['start_type'], partial_cds['rbs_motif'], partial_cds['aa_hexdigest'], partial_cds['sequence'][:10], partial_cds['sequence'][-10:]
            )
    return cdss


def split_gff_annotation(annotation_string):
    annotations = {}
    for expr in annotation_string.split(';'):
        if(expr != ''):
            try:
                key, value = expr.split('=')
                annotations[key] = value
            except:
                log.error('expr=%s', expr)
    return annotations
