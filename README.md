README
===========================

After transplanting pytorch to the RISC-V platform, we ran the test module of pytorch and saved the test log. Since there are so many test scripts and a lot of logs are generated, we use scripts to analysis the log files.

****

# How to use(Linux Environment on RISC-V)

1.Run the test module of pytorch, save the output logs

```
cd ./test
python ./run_test.py >> ./pytorch_test.log
```

![image-20231012103330764](/image/log_sample.png)

2.use this tool to analyse the output logs

```
python analysis.py -f pytorch_test.log
```

![image-20231012145415945](/image/process.png)

3.check the results

![image-20231012145740105](/image/result.png)