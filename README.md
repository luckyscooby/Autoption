# Autoption

Michael Leocádio @ 2021

[![Python](https://img.shields.io/static/v1?label=&message=Python&color=%23FBBF24&logo=Python)](https://)

[![Status - Archived](https://img.shields.io/badge/Status-Active-green)](https://)

- **Description**<br>
  Automatic binary options trading for IQOption

- **Reasoning**<br>
  Back in 2019 I came in contact with trading through IQOption. Since then I dicovered and experimented many tools,
  brokers and even APIs for automations. When I met TradingView and its powerful scripting platform (PineScript) I was
  amazed of the countless possibilities of strategy creation and backtesting, specially that other way more experienced
  traders would rather share their code. However I wanted to be able to automate the operations instead of waiting for
  the signals and run to the broker to place my order; when you work on very low timeframes (M1 or M5, for instance)
  every second after a signal is crucial, so nothing better than an automation script.<br><br>Then I found an unoficial
  API in Python for IQOption: https://github.com/iqoptionapi/iqoptionapi
  It worked like a charm, so I started experimenting with dozens of strategies taking the advantage of automated
  analysis and order placement (practicity and velocity).
  I even implemented machine learning based analysis over the candle series using the Prophet API for
  predictions (https://facebook.github.io/prophet/docs/quick_start.html) and even a Rational Quadratic Kernel function
  in PineScript translated into Python (https://www.tradingview.com/script/e0Ek9x99-KernelFunctions/) which is based on
  Nadaraya-Watson kernel regression.
  Due to personal matters I don't maintain the old code since 2022, anyway I kept on testing new strategies and
  technical analysis on TradingView, specially over the kernel regressor.<br><br>My latest experiment (2023) led me to
  great results on binary options using M5 timeframe; I will continue my work on this automator, which now I call
  Autoption, so I'll need to refactor the majority of the actual code and remove obsolete functions that won't be part
  of the new strategy. If you want to access and study my old code, feel free to grab the first
  commit: https://github.com/luckyscooby/Autoption/tree/old

- **Usage / Features**<br>
  I will not report here the usage of the old code as it is highly experimental and has many obsolete functions from
  previous strategies, so this section will only be updated once I refactor everything into my consistently working
  strategy.
