import sys, os
from copy_header import *

from waflib.Tools.compiler_c import c_compiler
from waflib.Tools.compiler_cxx import cxx_compiler

sys.path += [ 'backend/tools/waf-plugins' ]

def options(opt):
  opt.load('defaults')
  opt.load('compiler_c')
  opt.load('compiler_cxx')

def configure(conf):
  Copy()
  conf.load('defaults')
  conf.load('compiler_c')
  conf.load('compiler_cxx')
  conf.env.INCLUDES += [ 'backend/src', 'src' ]
  conf.env.INCLUDES += [ 'external/common/include', 'include' ]
  conf.env.CXXFLAGS += [ '-g', '-ldl', '-std=c++11']
  #conf.env.CXXFLAGS += [ '-g', '-lpthread', '-ldl']
  conf.check(lib='pthread', uselib_store='pthread')
  conf.check(lib='config++', uselib_store='config++')
  conf.check(lib='python2.7', uselib_store='python2.7')
  conf.check(lib='zmq', uselib_store='zmq')
  conf.check(lib='z', uselib_store='z')

from waflib.Build import BuildContext
class all_class(BuildContext):
  cmd = "all"
class pricer_class(BuildContext):
  cmd = "pricer"
class proxy_class(BuildContext):
  cmd = "proxy"
class mid_data_class(BuildContext):
  cmd = "mid_data"
class ctpdata_class(BuildContext):
  cmd = "ctpdata"
class ctporder_class(BuildContext):
  cmd = "ctporder"
class getins_class(BuildContext):
  cmd = "get_ins"
class simplemaker_class(BuildContext):
  cmd = "simplemaker"
class simplearb_class(BuildContext):
  cmd = "simplearb"
class backtest_class(BuildContext):
  cmd = "backtest"
class order_matcher_class(BuildContext):
  cmd = "order_matcher"
class demostrat_class(BuildContext):
  cmd = "demostrat"
from lint import add_lint_ignore

def build(bld):
  add_lint_ignore('external')
  add_lint_ignore('backend')
  if bld.cmd == "all":
    run_all(bld)
    return
  if bld.cmd == "pricer":
    run_pricer(bld)
    return
  if bld.cmd == "mid_data":
    run_mid_data(bld)
    return
  if bld.cmd == "proxy":
    run_proxy(bld)
    return
  if bld.cmd == "ctpdata":
    run_ctpdata(bld)
    return
  if bld.cmd == "ctporder":
    run_ctporder(bld)
    return
  if bld.cmd == "getins":
    run_getins(bld)
    return
  if bld.cmd == "simplemaker":
    run_simplemaker(bld)
    return
  if bld.cmd == "simplearb":
    run_simplearb(bld)
    return
  if bld.cmd == "backtest":
    run_backtest(bld)
    return
  if bld.cmd == "order_matcher":
    run_order_matcher(bld)
    return
  if bld.cmd == "demostrat":
    run_demostrat(bld)
    return
  else:
    print "error! " + str(bld.cmd)
    return

def run_ctpdata(bld):
  bld.read_shlib('nick', paths=['external/common/lib'])
  bld.read_shlib('thostmduserapi', paths=['external/ctp/lib'])
  bld.program(
    target = 'bin/ctpdata',
    source = ['src/ctpdata/main.cpp'],
    includes = ['external/ctp/include', 'external/zeromq/include'],
    use = 'zmq thostmduserapi nick pthread config++'
  )
def run_pricer(bld):
  bld.read_shlib('nick', paths=['external/common/lib'])
  bld.program(
    target = 'bin/data_pricer',
    source = ['src/pricer/main.cpp'],
    includes = ['external/zeromq/include'],
    use = 'zmq nick pthread config++'
  )
def run_ctporder(bld):
  bld.read_shlib('nick', paths=['external/common/lib'])
  bld.read_shlib('thosttraderapi', paths=['external/ctp/lib'])
  bld.program(
    target = 'bin/ctporder',
    source = ['src/ctporder/main.cpp',
              'src/ctporder/listener.cpp',
              'src/ctporder/token_manager.cpp',
              'src/ctporder/message_sender.cpp'],
    includes = ['external/ctp/include', 'external/zeromq/include'],
    use = 'zmq thosttraderapi nick pthread config++'
  )
def run_proxy(bld):
  bld.program(
    target = 'bin/data_proxy',
    source = ['src/data_proxy/main.cpp'],
    includes = ['external/zeromq/include'],
    use = 'zmq pthread config++'
  )
  bld.program(
    target = 'bin/order_proxy',
    source = ['src/order_proxy/main.cpp'],
    includes = ['external/zeromq/include'],
    use = 'zmq pthread config++'
  )

def run_mid_data(bld):
  bld.read_shlib('nick', paths=['external/common/lib'])
  bld.program(
    target = 'bin/mid_data',
    source = ['src/mid_data/main.cpp'],
    includes = ['external/zeromq/include'],
    use = 'zmq nick pthread config++'
  )

def run_getins(bld):
  bld.read_shlib('nick', paths=['external/common/lib'])
  bld.read_shlib('thosttraderapi', paths=['external/ctp/lib'])
  bld.program(
    target = 'bin/getins',
    includes = ['external/ctp/include', 'external/zeromq/include'],
    source = ['src/GetInstrument/main.cpp'],
    use = 'zmq nick thosttraderapi pthread config++'
  )

def run_simplemaker(bld):
  bld.read_shlib('nick', paths=['external/common/lib'])
  bld.program(
    target = 'bin/simplemaker',
    source = ['src/simplemaker/main.cpp',
              'src/simplemaker/strategy.cpp'],
    includes = ['external/zeromq/include'],
    use = 'zmq nick pthread config++'
  )

def run_simplearb(bld):
  #bld.read_shlib('nick', paths=['external/common/lib'])
  bld.read_shlib('nick', paths=['external/common/lib'])
  #bld.read_shlib('simplearb', paths=['external/strategy/simplearb/lib'])
  bld.program(
    target = 'bin/simplearb',
    source = ['src/simplearb/main.cpp',
              'src/simplearb/strategy.cpp'
             ],
    includes = [
                #'external/strategy/simplearb/include',
                'external/zeromq/include'
               ],
    use = 'zmq nick pthread config++ shm' # simplearb'
  )

def run_backtest(bld):
  bld.read_shlib('nick', paths=['external/common/lib'])
  #bld.read_shlib('backtest', paths=['external/strategy/backtest/lib'])
  bld.program(
    target = 'bin/backtest',
    source = ['src/backtest/main.cpp',
              'src/backtest/strategy.cpp'
             ],
    includes = [
                #'external/strategy/backtest/include',
                'external/zeromq/include'
                ],
    use = 'zmq nick pthread config++ python2.7 z'
  )

def run_order_matcher(bld):
  bld.read_shlib('nick', paths=['external/common/lib'])
  bld.program(
    target = 'bin/order_matcher',
    source = ['src/order_matcher/main.cpp',
              'src/order_matcher/order_handler.cpp'],
    includes = ['external/zeromq/include'],
    use = 'zmq nick pthread config++'
  )

def run_demostrat(bld):
  bld.read_shlib('nick', paths=['external/common/lib'])
  bld.program(
    target = 'bin/demostrat',
    source = ['src/demostrat/main.cpp',
              'src/demostrat/strategy.cpp'],
    includes = ['external/zeromq/include'],
    use = 'zmq nick pthread config++'
  )

def run_all(bld):
  #run_pricer(bld)
  run_mid_data(bld)
  run_proxy(bld)
  run_ctpdata(bld)
  run_ctporder(bld)
  run_getins(bld)
  run_simplearb(bld)
  run_backtest(bld)
  run_order_matcher(bld)
  run_demostrat(bld)
  run_simplemaker(bld)
