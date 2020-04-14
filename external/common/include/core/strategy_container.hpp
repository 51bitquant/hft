#ifndef STRATEGY_CONTAINER_HPP_
#define STRATEGY_CONTAINER_HPP_

#include <thread>
#include <vector>
#include <unordered_map>
#include <iostream>
#include <string>

#include "core/base_strategy.h"
#include "util/recver.hpp"
#include "util/shm_recver.hpp"

using namespace std;

// template<template<typename> typename T>
// template<template<class K> T>
template<template<typename> class T>
class StrategyContainer {
 public:
  StrategyContainer(unordered_map<string, vector<BaseStrategy*> > &m)
    : m(m),
      marketdata_recver(new T<MarketSnapshot>("data_pub")),
      exchangeinfo_recver(new T<ExchangeInfo>("exchange_info")),
      command_recver(new Recver<Command>("*:33334", "tcp", "bind")) {

}
  // explicit StrategyContainer(const StrategyContainer& sc) {}  // unable copy constructor
  // explicit StrategyContainer(StrategyContainer && sc) {}  // unable move constructor
  virtual ~StrategyContainer() {
  }
  void Start() {
    thread command_thread(RunCommandListener, std::ref(m), command_recver.get());
    thread exchangeinfo_thread(RunExchangeListener, std::ref(m), exchangeinfo_recver.get());
    thread marketdata_thread(RunMarketDataListener, std::ref(m), marketdata_recver.get());
    command_thread.join();
    exchangeinfo_thread.join();
    marketdata_thread.join();
  }
 private:
  static void RunCommandListener(unordered_map<string, vector<BaseStrategy*> > &m, Recver<Command>* command_recver) {
    while (true) {
      Command shot;
      command_recver->Recv(shot);
      printf("command recved!\n");
      shot.Show(stdout);
      string ticker = Split(shot.ticker, "|").front();
      if (ticker == "load_history") {
        // Load_history("mid.dat");
        continue;
      }
      vector<BaseStrategy*> sv = m[ticker];
      for (auto v : sv) {
        v->HandleCommand(shot);
      }
    }
  }

  static void RunExchangeListener(unordered_map<string, vector<BaseStrategy*> > &m, T<ExchangeInfo>* exchangeinfo_recver) {
    while (true) {
      ExchangeInfo info;
      exchangeinfo_recver->Recv(info);
      info.Show(stdout);
      std::vector<BaseStrategy*> sv = m[info.ticker];
      for (auto v : sv) {
        v->UpdateExchangeInfo(info);
      }
    }
  }

  static void RunMarketDataListener(unordered_map<string, vector<BaseStrategy*> > &m, T<MarketSnapshot> * marketdata_recver) {
    while (true) {
      MarketSnapshot shot;
      marketdata_recver->Recv(shot);
      auto sv = m[shot.ticker];
      for (auto s : sv) {
        s->UpdateData(shot);
      }
    }
  }

  unordered_map<string, vector<BaseStrategy*> > &m;
  unique_ptr<T<MarketSnapshot> > marketdata_recver;
  unique_ptr<T<ExchangeInfo> > exchangeinfo_recver;
  unique_ptr<Recver<Command> > command_recver;
};

#endif  // STRATEGY_CONTAINER_HPP_
