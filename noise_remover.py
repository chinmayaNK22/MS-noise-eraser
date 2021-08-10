## This tool is developed by Mr. Sandeep Kasargod, Mr. Santosh Kumar Behera and Mr. Chinmaya Narayana K.
## If you have any queries please contact chinmaya_k@yenepoya.edu.in

import argparse
import os

parser = argparse.ArgumentParser(description='''Remove MS/MS peaks below the threshold limit from a .mgf file''')

parser.add_argument('infile', metavar='-ip', type=str, nargs='+', help='MGF file path or path to multiple MGF files')

parser.add_argument('threshold', metavar='-t', type=float, nargs='+', help='m/z peaks with or less than the set threshold intensity values will be discarded')

args = parser.parse_args()

def read_mgf(infile):
    dicts_mz = {}
    dicts_mz_info = {}
    for i in open(os.path.join(infile)):
        if "BEGIN IONS" in i.rstrip():
            title = ""
            pepmass = ""
            rt = ""
            charge=""
            scans=""
            lst = []
        if "TITLE" in i.rstrip():
            file_name = i.split(' ')[1].split(':')[-1].strip('"')
            title = i.rstrip()
        if "PEPMASS" in i.rstrip():
            pepmass = i.rstrip()
        if "CHARGE" in i.rstrip():
            charge = i.rstrip()
        if "RTINSECONDS" in i.rstrip():
            rt = i.rstrip()
        if "SCANS" in i.rstrip():
            scans = i.rstrip()
        if len(i.rstrip()) > 2 and i.rstrip()[0].isdigit():
            lst.append(i.rstrip())
        if "END IONS" in i.rstrip():
            if file_name not in dicts_mz:
                dicts_mz[file_name] = [lst]
                dicts_mz_info[file_name] = [title + "@" + rt.rstrip() + "@" + pepmass + "@" + charge + "@" + scans]
            else:
                dicts_mz[file_name].append(lst)
                dicts_mz_info[file_name].append(title + "@" + rt.rstrip() + "@" + pepmass + "@" + charge + "@" + scans)

    print (str(len([s for k, v in dicts_mz.items() for s in v])) + " scans are extracted from the file " + os.path.split(infile)[-1] + " succesfully")
    return dicts_mz, dicts_mz_info

def remove_noise(infile, noise_threshold):
    spectrum, header = read_mgf(os.path.join(infile))
    output = []
    for k, v in spectrum.items():
        for iters in range(len(v)):
            dicts_mz_info_1 = header[k][iters].split('@')
            abundance = [float(o.split(' ')[-1]) for o in v[iters]]
            spectra = [o for o in v[iters] if float(o.split(' ')[-1])/max(abundance)*100 > float(noise_threshold)]
            output.append(["BEGIN IONS"] + dicts_mz_info_1 + spectra + ["END IONS"])

    return output

def noise_remover(inpath, threshold):
    if os.path.isfile(os.path.join(inpath)):
        if inpath.split('.')[-1] == 'mgf':
            if "noise_removed.mgf" not in inpath:
                output = remove_noise(inpath, threshold)
                outfile = "{0}_noise_removed.mgf".format(os.path.split(inpath)[-1].rstrip('.mgf'))    
                with open(outfile, 'w') as outf:
                    outf.writelines('\n'.join(i) + '\n' + '\n' for i in output)
    else:    
        infiles = []
        for mgf_files in os.listdir(inpath):
            if os.path.isfile(os.path.join(inpath, mgf_files)):
                if mgf_files.split('.')[-1] == 'mgf':
                    if "noise_removed.mgf" not in mgf_files:
                        infiles.append(os.path.join(inpath, mgf_files))
        
        for infile in infiles:
            output = remove_noise(infile, threshold)
            outfile = "{0}_noise_removed.mgf".format(os.path.split(infile)[-1].rstrip('.mgf'))    
            with open(outfile, 'w') as outf:
                outf.writelines('\n'.join(i) + '\n' + '\n' for i in output)

noise_remover(args.infile[0], args.threshold[0])
