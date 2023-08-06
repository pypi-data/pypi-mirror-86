import json
from os import makedirs, path
import requests
from Bio.PDB import parse_pdb_header

from py3pdb.utils import error
from py3pdb.download import download_pdb


def protein_sequence_search(aa_sequence, evalue_cutoff=1, identity_cutoff=1):

    page = """https://search.rcsb.org/rcsbsearch/v1/query?json=
              {"query": {"type": "terminal", "service": "sequence",
                         "parameters": {"evalue_cutoff": \"""" + str(evalue_cutoff) + """\", 
                                       "identity_cutoff": \"""" + str(identity_cutoff) + """\", 
                                       "target": "pdb_protein_sequence",
                                       "value": \"""" + str(aa_sequence) + """\"}},
               "request_options": {"scoring_strategy": "sequence"},
               "return_type": "polymer_entity"}"""

    req = requests.get(page)
    if req.status_code == 200:
        return json.loads(req.text)['result_set']
    else:
        error('[Protein Sequence Search] -> Website no response!')
        return None


def get_pdb(pss_result, if_full_match=True, if_best_resolution=True, if_download=True):
    outdir_pdb = './pdb_download'
    if not path.exists(outdir_pdb):
        makedirs(outdir_pdb)

    pdb_reso = []

    for r in pss_result:
        pdb_id = None
        pdb_full = None

        # fully matched or not
        if if_full_match:
            info = r['services'][0]['nodes'][0]['match_context'][0]
            if info['mismatches'] == 0 \
                    and info['gaps_opened'] == 0 \
                    and info['query_length'] == info['subject_length']:
                pdb_full = r['identifier']
                pdb_id = pdb_full.split('_')[0]
        else:
            pdb_full = r['identifier']
            pdb_id = pdb_full.split('_')[0]

        # if match, download pdb file
        if pdb_id and pdb_full:
            outfile = path.join(outdir_pdb, str(
                pdb_id) + '.pdb') if if_download else path.join(outdir_pdb, 'tmp.pdb')
            if download_pdb(pdb_id, outfile):
                structure = parse_pdb_header(outfile)
                pdb_reso.append((pdb_full, structure['resolution']))

    if if_best_resolution:
        # find the pdb with best resolution
        tmp_dict = {r: p for p, r in pdb_reso}
        best_pdb_id = tmp_dict[max(tmp_dict.keys())]
        return [(best_pdb_id, tmp_dict[best_pdb_id])]
        # write to file
        # with open('./dataset_pos.csv', 'a') as f:
        #     f.write("{}, {}, {}\n".format(best_pdb_id, seq, pdb_reso))
        #     print("{} - {}".format(i, pdb_reso))

    return pdb_reso



