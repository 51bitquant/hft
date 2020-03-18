#ifndef STRATEGY_H_
#define STRATEGY_H_

#include <struct/market_snapshot.h>
#include <struct/strategy_status.h>
#include <timecontroller.h>
#include <struct/order.h>
#include <util/sender.hpp>
#include <struct/exchange_info.h>
#include <struct/order_status.h>
#include <util/common_tools.h>
#include <core/base_strategy.h>
#include <libconfig.h++>
#include <unordered_map>

#include <cmath>
#include <vector>
#include <string>


class Strategy : public BaseStrategy {
 public:
  Strategy(const libconfig::Setting & setting, TimeController tc, std::unordered_map<std::string, std::vector<BaseStrategy*> >*ticker_strat_map, std::string mode = "real");
  ~Strategy();

  void Start();
  void Stop();

  void Clear();
 private:
  void DoOperationAfterUpdateData(MarketSnapshot shot);
  void DoOperationAfterUpdatePos(Order* o, ExchangeInfo info);
  void DoOperationAfterFilled(Order* o, ExchangeInfo info);
  void DoOperationAfterCancelled(Order* o);
  void ModerateOrders(std::string contract);
  void InitTicker();
  void InitTimer();
  bool Ready();
  void Pause();
  void Resume();
  void Run();
  void Train();
  void Flatting();

  double OrderPrice(std::string contract, OrderSide::Enum side, bool control_price);

  OrderSide::Enum OpenLogicSide();
  bool OpenLogic();
  void CloseLogic();

  void Open(OrderSide::Enum side);
  void Close(bool force_flat = false);

  bool TimeUp();

  void CalParams();
  bool HitMean();

  bool Spread_Good();

  bool IsAlign();
  char order_ref[MAX_ORDERREF_SIZE];
  std::string main_ticker;
  std::string hedge_ticker;
  int max_pos;
  double min_price;

  TimeController this_tc;
  int cancel_threshhold;
  std::unordered_map<std::string, double> mid_map;
  double up_diff;
  double down_diff;
  double mean;
  std::vector<double> map_vector;
  int current_pos;
  double min_profit;
  unsigned int min_train_sample;
  double min_range;
  double increment;
  std::string mode;
  double spread_threshold;
  int closed_size;
  int max_holding_sec;
  int build_position_time;
  double last_valid_mid;
};

#endif  // STRATEGY_H_
