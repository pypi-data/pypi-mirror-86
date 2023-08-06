from typing import Union, List, Optional
from numpy import array
from jinfo.sequence import BaseSeq, DNASeq, RNASeq, AASeq
from jinfo.alignment import BaseAlignment
from jinfo.phylogenetics import PhyloTree


ALL_SEQS = Union[BaseSeq, DNASeq, RNASeq, AASeq]


def DNASeq_from_NCBI(NCBI_accession: str) -> DNASeq:
    """
    Fetch a DNA sequence using the NCBI Entrez api

    Returns jinfo.DNASeq object
    """

    return DNASeq()


def alignment_from_fasta(file_path: str, seq_obj: ALL_SEQS = BaseSeq) -> BaseAlignment:
    """
    Parse alignment from fasta file

    Returns Alignment object
    """

    from jinfo.utils.seq_list_from_fasta import seq_list_from_fasta

    seq_list = seq_list_from_fasta(file_path=file_path, seq_obj=seq_obj)
    return BaseAlignment(aligned_sequences=seq_list)


class FastTree2NotInstalledError(Exception):
    pass


def calc_phylo_tree(alignment_obj: BaseAlignment) -> PhyloTree:
    """
    Calculate a Newick format phylogenetic tree from an alignment object

    ***Requires FastTree2 package***
    Returns: Tree object
    """

    import subprocess
    from jinfo.utils.seq_list_to_fasta import seq_list_to_fasta

    try:
        test_cmd = "FastTreeMP".split(" ")
        subprocess.run(test_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise FastTree2NotInstalledError

    in_path = "temp.fasta"
    out_path = "temp.tree"
    seq_list_to_fasta(
        seq_list=alignment_obj.seqs, file_name=in_path, label_list=alignment_obj.labels
    )

    bash_cmd = f"FastTreeMP {in_path}".split(sep=" ")
    with open(out_path, "w") as text_file:
        subprocess.run(bash_cmd, stdout=text_file)

    with open(out_path, "r") as text_file:
        tree_obj = PhyloTree(text_file.read())

    cleanup_cmd = f"rm {in_path} {out_path}".split(sep=" ")
    subprocess.run(cleanup_cmd)
    return tree_obj


class MuscleNotInstalledError(Exception):
    pass


def multialign(seq_list: List[ALL_SEQS], maxiters: int = 16) -> BaseAlignment:
    """
    Perform multiple sequence alignment, optionally control the number of iterations

    ***Requires MUSCLE package***
    Returns Alignment object
    """

    import subprocess
    from jinfo.utils.seq_list_to_fasta import seq_list_to_fasta
    from jinfo.utils.alignment_from_fasta import alignment_from_fasta

    try:
        test_cmd = "muscle -quiet".split(" ")
        subprocess.run(test_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise MuscleNotInstalledError

    in_path = "_temp.fasta"
    out_path = "_temp2.fasta"
    seq_list_to_fasta(seq_list=seq_list, file_name=in_path, label_list=None)
    bash_cmd = (
        f"muscle -in {in_path} -out {out_path} -quiet -maxiters {maxiters}".split(
            sep=" "
        )
    )
    subprocess.run(bash_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    alignment_obj = alignment_from_fasta(out_path, seq_obj=type(seq_list[0]))
    cleanup_cmd = f"rm {in_path} {out_path}".split(sep=" ")
    subprocess.run(cleanup_cmd)
    return alignment_obj


class SeqLengthError(Exception):
    pass


def one_hot_dna(seq_obj: DNASeq, max_seq_len: int) -> array:
    """
    One hot encode a DNASeq sequence for ML applications.

    Add zero padding up to the maximum length.
    Returns: 1D numpy array of length 4*max_seq_len
    """

    import numpy as np

    if seq_obj.len > max_seq_len:
        raise SeqLengthError("DNASeq.len exceeds max_seq_len")

    encode_dict = {
        "A": [1, 0, 0, 0],
        "T": [0, 1, 0, 0],
        "C": [0, 0, 1, 0],
        "G": [0, 0, 0, 1],
        "X": [0, 0, 0, 0],
    }
    padding = "".join(["X" for i in range(max_seq_len - seq_obj.len)])
    encoded_dna = [encode_dict[base] for base in seq_obj.seq + padding]
    np_encoded = np.array(encoded_dna, dtype=int)
    return np_encoded.flatten()


def percentage_identity(seq1: ALL_SEQS, seq2: ALL_SEQS, dp: int = 2) -> float:
    """
    Calculate pairwise sequence similarity from aligned sequences

    Optionally control precision using dp argument
    Returns: float
    """
    i = 0
    for b1, b2 in zip(seq1.seq, seq2.seq):
        if b1 == b2:
            i += 1
    pid = i * 100 / ((seq1.len + seq2.len) / 2)
    return round(pid, dp)


class HmmerNotInstalledError(Exception):
    pass


def seq_id_from_hmmer(result_path: str, seq_obj: ALL_SEQS = BaseSeq) -> ALL_SEQS:
    """"""

    return seq_obj()


def phmmer(seq_list: List[ALL_SEQS], query_seq: ALL_SEQS) -> ALL_SEQS:
    """

    ***Requires hmmer package***
    Returns:
    """

    import subprocess
    import multiprocessing as mp
    from jinfo.utils.seq_list_to_fasta import seq_list_to_fasta
    from jinfo.utils.seq_list_from_fasta import seq_list_from_fasta

    try:
        test_cmd = "phmmer".split(" ")
        subprocess.run(test_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise HmmerNotInstalledError

    q_path = "_hmmer_temp_query.fasta"
    db_path = "_hmmer_temp_db.fasta"
    out_path = "_hmmer_temp_out.txt"

    query_seq.save_fasta(q_path)
    seq_list_to_fasta(seq_list=seq_list, file_name=db_path, label_list=None)

    bash_cmd = f"phmmer {q_path} {db_path} -o {out_path} -cpu {mp.cpu_count()}".split(
        sep=" "
    )
    subprocess.run(bash_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Get result from hmmer output fule...
    hit_id = seq_id_from_hmmer(out_path)
    output_seq_obj = 0

    cleanup_cmd = f"rm {q_path} {db_path} {out_path}".split(sep=" ")
    subprocess.run(cleanup_cmd)
    return


def random_DNASeq(seq_length: int) -> DNASeq:
    """
    Generate a random DNA sequence

    Returns: random DNASeq of length seq_length
    """

    import random
    from jinfo.sequence import DNASeq

    dna_base_list = ["A", "T", "C", "G"]
    seq_list = [random.choice(dna_base_list) for i in range(seq_length)]
    return DNASeq(sequence="".join(seq_list))


def remove_degenerate_seqs(
    alignment_obj: BaseAlignment, identity_limit: int, show_id_array: bool = False
) -> BaseAlignment:
    """
    Filter high similarity sequences from a list of Seq objects

    Returns: BaseAlignment
    """
    import multiprocessing as mp
    from functools import partial
    from jinfo.utils.percentage_identity import percentage_identity

    seq_list = alignment_obj.seqs
    identity_array = []
    filtered_seqs = []
    pool = mp.Pool(mp.cpu_count())  # Set up cpu pool for parallel calculation

    for seq_obj in seq_list:
        id_partial = partial(percentage_identity, seq2=seq_obj)
        identity_array_row = pool.map(id_partial, seq_list)
        identity_array.append(identity_array_row)

    if show_id_array:
        print("Calculated alignment identity array:")
        for i, row in enumerate(identity_array):
            print(f"{seq_list[i].label}\t{row}")

    for i, row in enumerate(identity_array):
        row.remove(100)  # remove seq 100% match with itself
        if max(row) < float(identity_limit):
            filtered_seqs.append(seq_list[i])

    return BaseAlignment(filtered_seqs)


def seq_from_fasta(file_path: str, seq_type: Optional[ALL_SEQS]) -> ALL_SEQS:
    """
    Parse a fasta file

    Returns specified type of Seq object
    """

    import re
    from jinfo.sequence import BaseSeq, DNASeq, RNASeq, AASeq

    with open(file_path, "r") as text_file:
        fasta_str = text_file.read()

    label = re.findall(r"^>(.*)", fasta_str)[0]
    fasta_lines = fasta_str.split("\n")
    label_index = fasta_lines.index(">" + label)
    seq_string = "".join(fasta_lines[label_index + 1 :])
    if seq_type is None:
        return BaseSeq(sequence=seq_string, label=label)
    else:
        return seq_type(sequence=seq_string, label=label)


def seq_list_from_fasta(file_path: str, seq_obj: ALL_SEQS) -> List[ALL_SEQS]:
    """
    Parse a multifasta file

    Returns list of BaseSeq objects
    """

    from jinfo.sequence import BaseSeq
    import re

    with open(file_path, "r") as text_file:
        fasta_str = text_file.read()

    label_list = re.findall(r"^>(.*)", fasta_str, re.MULTILINE)
    fasta_lines = fasta_str.split("\n")
    seq_list = []

    for i in range(len(label_list)):
        label_index = fasta_lines.index(">" + label_list[i])
        if i == len(label_list) - 1:
            seq_string = "".join(fasta_lines[label_index + 1 :])
        else:
            next_label_index = fasta_lines.index(">" + label_list[i + 1])
            seq_string = "".join(fasta_lines[label_index + 1 : next_label_index])

        seq_list.append(seq_obj(sequence=seq_string, label=label_list[i]))
    return seq_list


def seq_list_to_fasta(
    seq_list: List[ALL_SEQS], file_name: Optional[str], label_list: Optional[List[str]]
) -> str:
    """
    Convert a list of Seq objects to a fasta format string

    Optionally add labels and save to file
    Returns: fasta string
    """

    fasta_str = ""
    for i, seq_obj in enumerate(seq_list):
        if label_list:
            label = label_list[i]
        elif seq_obj.label != "":
            label = seq_obj.label
        else:
            label = f"Sequence_{i}"
        fasta_str += f">{label}\n{seq_obj.seq}\n\n"

    if file_name:
        with open(file=file_name, mode="w") as text_file:
            text_file.write(fasta_str)
    return fasta_str


if __name__ == "__main__":
    pass
