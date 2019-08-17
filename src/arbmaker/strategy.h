#ifndef SRC_ARBMAKER_STRATEGY_H_
#define SRC_ARBMAKER_STRATEGY_H_

#include <market_snapshot.h>
#include <timecontroller.h>
#include <order.h>
#include <sender.h>
#include <exchange_info.h>
#include <order_status.h>
#include <common_tools.h>
#include <base_strategy.h>
#include <unordered_map>

#include <cmath>
#include <vector>
#include <string>


class Strategy : public BaseStrategy {
 public:
  Strategy(std::string main_ticker, std::string hedge_ticker, int maxpos, double tick_size, TimeController tc, int contract_size, std::string strat_name, bool enable_stdout = true, bool enable_file = true);
  ~Strategy();

  void Start();
  void Stop();
 private:
  void DoOperationAfterUpdatePos(Order* o, ExchangeInfo info);
  void DoOperationAfterUpdateData(MarketSnapshot shot);
  void DoOperationAfterFilled(Order* o, ExchangeInfo info);
  void DoOperationAfterCancelled(Order* o);
  double OrderPrice(std::string contract, OrderSide::Enum side, bool control_price);
  bool IsReady();

  bool IsHedged();
  bool MidBuy();
  bool IsAlign();
  bool MidSell();

  bool IsParamOK();
  bool Spread_Good();
  void ModerateHedgeOrders();
  void ModerateOrders(std::string contract, double edurance);

  double CalBalancePrice();

  bool TradeClose(std::string contract, int size);

  bool PriceChange(double current_price, double reasonable_price, OrderSide::Enum side, double edurance);

  void AddCloseOrderSize(OrderSide::Enum side);

  char order_ref[MAX_ORDERREF_SIZE];
  std::string main_ticker;
  std::string hedge_ticker;
  int max_pos;
  double poscapital;
  double min_price;
  double price_control;
  double edurance;
  TimeController m_tc;

  pthread_mutex_t add_size_mutex;
  int cancel_threshhold;
  bool is_stopped;
  int count;
  std::unordered_map<std::string, double> mid_map;
  std::unordered_map<std::string, Order*> sleep_order_map;
  double up_diff;
  double down_diff;
  std::vector<double> map_vector;
  double max_spread;
  unsigned int min_train_sample;
};

#endif  // SRC_ARBMAKER_STRATEGY_H_
