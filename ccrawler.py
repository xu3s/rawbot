import os
import re
#from zipfile import ZipFile
import shutil
import uptobox
from comiccrawler.mission import Mission
from comiccrawler.analyzer import Analyzer
from comiccrawler.crawler import download

# m = Mission(url="https://manga.bilibili.com/detail/mc29562?from=manga_index")
# Analyzer(m).analyze()
savepath = "/data/data/com.termux/files/home/developing/discord/saved"

def mdownload(url,chan=None):
    m = Mission(url=url)
    Analyzer(m).analyze()
    title = m.title

    if chan is None:
        return [f'series title: {title}, chapter total:{len(m.episodes)}']
    chlist = chan_gen(chan)

    ttl = []
    for ep in m.episodes:
        if int(re.findall(r"\d+", ep.title)[0]) not in chlist:
            ep.skip = True
            continue
        ttl.append(ep.title)
    #return ttl
    if ttl not in uptobox.get_list(title):
        download(m, savepath)

        zprr = []
        for ept in ttl:
            result = zpr(series_title=title,
                    filename=ept,
                    dest=f'{savepath}/{title}',
                    to_zip=f'{savepath}/{title}/{ept}')
            zprr.append('{title} - {ept}:')
            zprr.append(result)
        return zprr

    rlink = []
    for ch_title in ttl:
        rlink.append(f'{title} - {ch_title}:')
        rlink.append(uptobox.get_link(title, ch_title))
    return rlink

def chan_gen(strnum):
    """ Generate chapter number from format 1,3-4,6
    or something like that
    :return: list of number [1,3,4,6]
    """

    if "," in strnum:
        a = strnum.split(',')
    else:
        a = [strnum]

    result = []
    for x in a:
        if '-' in x:
            xr = x.split('-')
            for b in range(int(xr[0]), int(xr[1])+1):
                result.append(b)
            continue
        result.append(int(x))
    return result


def zpr(filename, series_title,  dest, to_zip):

    local_path = f'{dest}/zipped/{filename}'
    if not os.path.isfile(f'{local_path}.zip'):
        try:
            shutil.make_archive(f'{dest}/zipped/{filename}',
                'zip', to_zip)
        except Exception as e: # pylint: disable=broad-except
            print(e)
            return f'something wrong with {filename}'
    uptobox.upload(series_title, filename, f'{local_path}.zip')
    rlink = uptobox.get_link(series_title, filename)
    return rlink


#   try:
#       with ZipFile(f'{dest}/{filename}.zip', 'w') as wzip:
#           wzip.write(to_zip)
#       return f'zipped to {dest}'
#   except Exception as e:
#       return e


if __name__ == "__main__":
    link = "https://manga.bilibili.com/detail/mc29562?from=manga_index"
    numb = "1-3"
    print(mdownload(link,numb))
#download(m, "/data/data/com.termux/files/home/developing/discord/saved")

