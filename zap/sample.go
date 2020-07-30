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

func initLoggers() {
	ec := zapcore.EncoderConfig{
		// Keys can be anything except the empty string.
		TimeKey:        "T",
		LevelKey:       "L",
		NameKey:        "N",
		CallerKey:      "C",
		MessageKey:     "M",
		StacktraceKey:  "S",
		LineEnding:     zapcore.DefaultLineEnding,
		EncodeLevel:    zapcore.CapitalColorLevelEncoder,
		EncodeTime:     zapcore.ISO8601TimeEncoder,
		EncodeDuration: zapcore.StringDurationEncoder,
		EncodeCaller:   zapcore.ShortCallerEncoder,
	}

	core := zapcore.NewCore(zapcore.NewConsoleEncoder(ec), os.Stdout, zap.DebugLevel)
	options := []zap.Option{
		zap.AddStacktrace(zap.WarnLevel),
		zap.WithCaller(true),
	}
	logger := zap.New(core, options...)
	DebugLogger = logger.Sugar()
	DefaultLogger = logger.WithOptions(zap.IncreaseLevel(zap.InfoLevel)).Sugar()

	zap.ReplaceGlobals(DefaultLogger.Desugar())
}

func main() {
	initLoggers()

	defer DefaultLogger.Sync()

	DefaultLogger.Debug("debug log from default logger")
	DefaultLogger.Error("error log from default logger")

	DebugLogger.Debug("debug log from debug logger")
	DebugLogger.Error("error log from debug logger")

	zap.S().Info("info log from zap.S()")
}
