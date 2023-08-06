# Copyright (C) 2020 Crane Chu <cranechu@gmail.com>
# This file is part of pynvme's conformance test
#
# pynvme's conformance test is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# pynvme's conformance test is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pynvme's conformance test. If not, see
# <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-


import time
import pytest
import logging

from scripts.psd import IOCQ, IOSQ, PRP, PRPList, SQE, CQE


def test_pcie_identifiers(pcie):
    logging.info("Identifiers: 0x%x" % pcie.register(0))
    logging.info("Subsystem Identifiers: 0x%x" % pcie.register(0x2c))
    
    
def test_pcie_command(pcie):
    logging.info("Command: 0x%x" % pcie.register(4, 2))
    #check Memory Space Enable = 1
    assert pcie.register(4, 2)&0x2 != 0   
    #check reserved field
    assert pcie.register(4, 2)&0xf800 == 0

    
def test_pcie_revision_id(pcie):
    logging.info("Revision ID: 0x%x" % pcie.register(8, 1))

    
def test_pcie_class_code(pcie):
    logging.info("Class Code: 0x%x" % pcie.register(9, 3))
    assert pcie.register(9, 3) == 0x010802

    
def test_pcie_bist(pcie):
    logging.info("Builtin self test: 0x%x" % pcie.register(0xf, 1))
    assert pcie.register(0xf, 1) == 0
    
    
def test_pcie_pmcr(pcie):
    pmcr_addr = pcie.cap_offset(0x01)
    pmcr = pcie.register(pmcr_addr, 4)
    logging.info("pmcr register [0x%x]= 0x%x"% (pmcr_addr, pmcr))
    logging.info("Version: %d" % ((pmcr>>16)&7))
    logging.info("AUX currect %d" % ((pmcr>>22)&7))

    
def test_pcie_pmcsr(pcie):
    pmcsr_addr = pcie.cap_offset(0x01)+4
    pmcsr = pcie.register(pmcsr_addr, 4)
    logging.info("pmcsr register [0x%x]= 0x%x"% (pmcsr_addr, pmcsr))
    logging.info("power state %d" % ((pmcsr>>0)&3))
    logging.info("no soft reset: %d" % ((pmcsr>>3)&1))

    scale = (pmcsr>>13)&0x3
    if scale:
        data = (pmcsr>>24)&0xff
        logging.info("D0 power consumption: %d mW" % (data*1000*(0.1**scale)))
    

def test_pcie_pcie_cap(pcie):
    pciecap_addr = pcie.cap_offset(0x10)
    pciecap = pcie.register(pciecap_addr, 4)
    logging.info("pcie capability register [0x%x]= 0x%x"% (pciecap_addr, pciecap))
    logging.info("capability version: %d" % ((pciecap>>16)&0x7))
    logging.info("device type: %d" % ((pciecap>>20)&0xf))
    logging.info("slot: %d" % ((pciecap>>24)&0x1))

    devcap = pcie.register(pciecap_addr+4, 4)
    logging.info("device capability register: 0x%x" % devcap)
    logging.info("Max_Payload_Size Supported: %d Byte" % (128*(2**(devcap&0x7))))

    devctrl = pcie.register(pciecap_addr+8, 2)
    logging.info("device control register: 0x%x" % devctrl)
    logging.info("relaxed ordering: %d" % ((devctrl>>4)&1))
    logging.info("Max_Payload_Size: %d Byte" % (128*(2**((devctrl>>5)&0x7))))
    logging.info("Max_Read_Request_Size: %d Byte" % (128*(2**((devctrl>>12)&0x7))))

    devsts = pcie.register(pciecap_addr+10, 2)
    logging.info("device status register: 0x%x" % devsts)
    pcie[pciecap_addr+10] = 1
    devsts = pcie.register(pciecap_addr+10, 2)
    logging.info("cleared correectable error detected bit")
    logging.info("device status register: 0x%x" % devsts)

    
def test_pcie_link_capabilities_and_status(pcie):
    linkcap_addr = pcie.cap_offset(0x10)+12
    linkcap = pcie.register(linkcap_addr, 4)
    logging.info("link capability register [0x%x]= 0x%x"% (linkcap_addr, linkcap))    
    logging.info("max link speed: %d"% ((linkcap>>0)&0xf))
    logging.info("max link width: %d"% ((linkcap>>4)&0x3f))
    logging.info("ASPM Support: %d"% ((linkcap>>10)&0x3))

    linkctrl_addr = pcie.cap_offset(0x10)+16
    linkctrl = pcie.register(linkctrl_addr, 2)
    logging.info("link control register [0x%x]= 0x%x"% (linkctrl_addr, linkctrl))    
    
    linksts_addr = pcie.cap_offset(0x10)+18
    linksts = pcie.register(linkcap_addr, 2)
    logging.info("link status register [0x%x]= 0x%x"% (linksts_addr, linksts))
    logging.info("link speed: %d"% ((linksts>>0)&0xf))
    logging.info("link width: %d"% ((linksts>>4)&0x3f))
    logging.info("link training: %d"% ((linksts>>11)&0x1))
    logging.info("link active: %d"% ((linksts>>13)&0x1))

    
@pytest.mark.parametrize("aspm", [0, 2])
def test_pcie_link_control_aspm(nvme0, pcie, aspm): #1:0
    linkctrl_addr = pcie.cap_offset(0x10)+16
    linkctrl = pcie.register(linkctrl_addr, 2)
    logging.info("link control register [0x%x]= 0x%x" %
                 (linkctrl_addr, linkctrl))

    # set ASPM control
    pcie[linkctrl_addr] = (linkctrl&0xfc)|aspm
    linkctrl = pcie.register(linkctrl_addr, 2)
    logging.info("link control register [0x%x]= 0x%x" %
                 (linkctrl_addr, linkctrl))

    # IO queue for read commands
    cq = IOCQ(nvme0, 1, 16, PRP())
    sq = IOSQ(nvme0, 1, 16, PRP(), cqid=1)

    # read lba 0 for 1000 times, interleaved with delays
    read_cmd = SQE(2, 1)
    read_cmd.prp1 = PRPList()
    pbit = 1
    for i in range(100):
        logging.debug(i)
        slot = i%16
        if slot == 0:
            pbit = not pbit
        next_slot = slot+1
        if next_slot == 16:
            next_slot = 0
        sq[slot] = read_cmd
        sq.tail = next_slot
        while cq[slot].p == pbit: pass
        cq.head = next_slot

        # delay to trigger ASPM
        time.sleep(0.01)

    sq.delete()
    cq.delete()

    time.sleep(1)
    
    #return ASPM L0
    pcie[linkctrl_addr] = (linkctrl&0xfc)|0
    

@pytest.mark.skip(reason="subsystem")
def test_pcie_cold_reset(subsystem, nvme0, buf):
    nvme0.identify(buf).waitdone()
    subsystem.power_cycle()
    nvme0.reset()
    nvme0.identify(buf).waitdone()


def test_pcie_format(nvme0n1):
    nvme0n1.format()

    
def test_pcie_read_bandwidth(nvme0n1):
    io_size = 128
    r = nvme0n1.ioworker(io_size=io_size,
                         lba_random=False,
                         read_percentage=100,
                         time=1).start().close()
    logging.debug(r)
    logging.info("%dMB/s" % ((io_size*512*r.io_count_read/1000)/1000))
    

@pytest.mark.parametrize("aspm", [0, 2])
@pytest.mark.parametrize("gen", [1, 2, 3, 2, 1, 1, 2, 3])
def test_pcie_link_speed(pcie, nvme0, nvme0n1, gen, aspm):
    linkctr2_addr = pcie.cap_offset(0x10)+0x30
    linkctr2 = pcie.register(linkctr2_addr, 4)
    logging.info(linkctr2)

    pcie[linkctr2_addr] = (linkctr2 & 0xf0) | gen
    logging.info(pcie.register(linkctr2_addr, 4))
    pcie.reset()
    nvme0.reset()
    test_pcie_read_bandwidth(nvme0n1)
    test_pcie_link_control_aspm(nvme0, pcie, aspm)
    

@pytest.mark.parametrize("gen", [5, 4, 0, 3])
def _test_pcie_link_speed_invalid(pcie, nvme0, nvme0n1, gen):
    linkctr2_addr = pcie.cap_offset(0x10)+0x30
    linkctr2 = pcie.register(linkctr2_addr, 4)
    logging.info(linkctr2)

    pcie[linkctr2_addr] = (linkctr2 & 0xf0) | gen
    logging.info(pcie.register(linkctr2_addr, 4))
    pcie.reset()
    nvme0.reset()
    
