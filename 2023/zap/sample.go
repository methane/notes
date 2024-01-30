package main

import (
	"os"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

var (
	// Debugが出力されるLogger
	DebugLogger *zap.SugaredLogger
	// 通常のLogger
	DefaultLogger *zap.SugaredLogger
)

func initLoggers() func() {
	consoleEnc := zap.NewDevelopmentEncoderConfig()
	core1 := zapcore.NewCore(zapcore.NewConsoleEncoder(consoleEnc), os.Stdout, zap.DebugLevel)

	sink, closer, err := zap.Open("/tmp/zaplog.out")
	if err != nil {
		panic(err)
	}
	fileEnc := zap.NewProductionEncoderConfig()
	core2 := zapcore.NewCore(zapcore.NewJSONEncoder(fileEnc), sink, zap.DebugLevel)

	core := zapcore.NewTee(core1, core2)

	options := []zap.Option{
		zap.AddStacktrace(zap.WarnLevel),
		zap.WithCaller(true),
	}
	logger := zap.New(core, options...)

	DebugLogger = logger.Sugar()
	DefaultLogger = logger.WithOptions(zap.IncreaseLevel(zap.InfoLevel)).Sugar()
	zap.ReplaceGlobals(logger)
	zap.RedirectStdLog(logger)

	return func() {
		logger.Sync()
		closer()
	}
}

func main() {
	defer initLoggers()()

	DefaultLogger.Debug("debug log from default logger")
	DefaultLogger.Error("error log from default logger")

	DebugLogger.Debug("debug log from debug logger")
	DebugLogger.Error("error log from debug logger")

	zap.S().Info("info log from zap.S()")
}
