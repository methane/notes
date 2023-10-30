for i in 1.0 0.5 0.1 0.05 0.0
do
    #time python ./otel-sampling.py $i > /dev/null
    time python ./otel-events.py $i > /dev/null
done
