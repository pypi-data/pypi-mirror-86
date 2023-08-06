import requests


def download_pdb(pdb_id, outfile):
    page = 'http://files.rcsb.org/view/{}.pdb'.format(pdb_id)
    req = requests.get(page)
    if req.status_code == 200:
        response = req.text
        if outfile:
            with open(outfile, 'w') as f:
                f.write(response)
        return 1
    else:
        return 0

