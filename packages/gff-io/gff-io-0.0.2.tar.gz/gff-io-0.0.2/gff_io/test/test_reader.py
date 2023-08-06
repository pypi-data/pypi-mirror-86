import os
import tarfile
from pathlib import Path

import importlib_resources as pkg_resources
import pytest

import gff_io


def test_read_example1(data_dir: Path):
    os.chdir(data_dir)

    with gff_io.read_gff("example1.gff") as file:
        assert file.header == "##gff-version 3"

        item = file.read_item()
        assert item.seqid == "AE014075.1:190-252|dna"
        assert item.source == "iseq"
        assert item.type == "."
        assert item.start == "1"
        assert item.end == "63"
        assert item.interval.start == 0
        assert item.interval.end == 63
        assert item.score == "0.0"
        assert item.strand == "+"
        assert item.phase == "."
        msg = "ID=item1;Target_alph=dna;Profile_name=Leader_Thr;Profile_alph=dna;"
        msg += "Profile_acc=PF08254.12;Window=0;Bias=17.5;E-value=2.9e-14;"
        msg += "Epsilon=0.01;Score=38.8"
        assert item.attributes == msg

        item = file.read_item()
        assert item.seqid == "AE014075.1:534-908|dna"
        assert item.source == "iseq"
        assert item.type == "."
        assert item.start == "1"
        assert item.end == "306"
        assert item.interval.start == 0
        assert item.interval.end == 306
        assert item.score == "0.0"
        assert item.strand == "+"
        assert item.phase == "."
        msg = "ID=item2;Target_alph=dna;Profile_name=Y1_Tnp;Profile_alph=dna;"
        msg += "Profile_acc=PF01797.17;Window=0;Bias=0.0;E-value=1.7e-29;"
        msg += "Epsilon=0.01;Score=88.6"
        assert item.attributes == msg

        with pytest.raises(StopIteration):
            file.read_item()


def test_read_example2(data_dir: Path):
    os.chdir(data_dir)

    items = list(gff_io.read_gff("example2.gff"))
    assert len(items) == 9
    item = items[-1]
    assert item.seqid == "2"
    assert item.source == "Prodigal:002006"
    assert item.type == "CDS"
    assert item.start == "5915"
    assert item.end == "6127"
    assert item.interval.start == 5914
    assert item.interval.end == 6127
    assert item.interval.to_rinterval().start == 5915
    assert item.interval.to_rinterval().end == 6127
    interval = item.interval
    interval = interval.offset(-5914)
    assert interval.start == 0
    assert interval.end == 213
    assert item.score == "."
    assert item.strand == "-"
    assert item.phase == "0"
    assert item.attributes[:30] == "ID=GALNBKIG_01033;inference=ab"

    with gff_io.read_gff("example2.gff") as file:
        items = file.read_items()
        assert len(items) == 9
        item = items[-1]
        assert item.seqid == "2"
        assert item.source == "Prodigal:002006"
        assert item.type == "CDS"
        assert item.start == "5915"
        assert item.end == "6127"
        assert item.interval.start == 5914
        assert item.interval.end == 6127
        assert item.score == "."
        assert item.strand == "-"
        assert item.phase == "0"
        assert item.attributes[:30] == "ID=GALNBKIG_01033;inference=ab"


def test_read_example3(data_dir: Path):
    os.chdir(data_dir)

    items = list(gff_io.read_gff("example3.gff"))
    assert len(items) == 0


def test_read_corrupted1(data_dir: Path):
    os.chdir(data_dir)

    with gff_io.read_gff("corrupted1.gff") as file:
        with pytest.raises(gff_io.ParsingError):
            file.read_item()


def test_read_corrupted2(data_dir: Path):
    os.chdir(data_dir)

    file = gff_io.read_gff("corrupted2.gff")
    file.read_item()
    file.read_item()
    file.read_item()
    file.read_item()
    file.read_item()
    file.read_item()
    file.read_item()
    file.read_item()
    file.read_item()
    with pytest.raises(gff_io.ParsingError):
        file.read_item()
    file.close()


def test_read_corrupted3(data_dir: Path):
    os.chdir(data_dir)

    with pytest.raises(gff_io.ParsingError):
        gff_io.read_gff("corrupted3.gff")


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    os.chdir(tmp_path)

    content = pkg_resources.read_binary(gff_io.test, "examples.tar.gz")

    with open("examples.tar.gz", "wb") as f:
        f.write(content)

    tar = tarfile.open("examples.tar.gz", "r:gz")
    tar.extractall()
    tar.close()

    os.unlink("examples.tar.gz")

    return tmp_path
