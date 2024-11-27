package com.example.bigdata;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.IOException;

public class FifaPlayers extends Configured implements Tool {

    public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new FifaPlayers(), args);
        System.exit(res);
    }

    public int run(String[] args) throws Exception {
        Job job = Job.getInstance(getConf(), "Fifaplayers");
        job.setJarByClass(this.getClass());
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        job.setMapperClass(CustomMapper.class);
        job.setReducerClass(CustomReducer.class);
        job.setCombinerClass(CustomCombiner.AAclass);

        job.setMapOutputKeyClass(IntWritaAble.class);
        job.setMapOutputValueClass(EarningsAgeCount.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);
        return job.waitForCompletion(true) ? 0 : 1;
    }

    public static class CustomMapper extends Mapper<LongWritable, Text, IntWritable, EarningsAgeCount> {

        private final IntWritable league = new IntWritable();
        private final DoubleWritable earnings = new DoubleWritable();
        private final IntWritable age = new IntWritable();
        private final IntWritable count = new IntWritable(1);

        private final EarningsAgeCount earningsAgeCount = new EarningsAgeCount(0.0,0,0);

        public void map(LongWritable offset, Text lineText, Context context) {
            try {
                if (offset.get() != 0) {
                    String line = lineText.toString();
                    int i = 0;
                    for (String word : line
                            .split(";(?=([^\"]*\"[^\"]*\")*[^\"]*$)")) {
                        if(i == 11){
                            earnings.set(Double.parseDouble(word));
                        }
                        if(i==12){
                            age.set(Integer.parseInt(word));
                        }
                        if(i==16){
                            league.set(Integer.parseInt(word));
                        }
                        if (i == 15) {
                            // weight over 100kg
                            if(Double.parseDouble(word)>100.0){
                                return;
                            }
                        }
//                        if (i == 5) {
//                            size.set(Double.parseDouble(word));
//                            earningsAgeCount.set(size,one);
//                        }
                        i++;
                    }

                    earningsAgeCount.set(earnings,age,count);
                    context.write(league, earningsAgeCount);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public static class CustomReducer extends Reducer<IntWritable, EarningsAgeCount, IntWritable, Text> {
        private final Text resultValue = new Text("");

        Double count;
        Double sumEarnings;
        Double avgEarnings;
        Double sumAge;
        Double avgAge;

        @Override
        public void reduce(IntWritable key, Iterable<EarningsAgeCount> values,
                           Context context) throws IOException, InterruptedException {

            avgEarnings = 0.0;
            sumEarnings = 0.0;

            avgAge = 0.0;
            sumAge = 0.0;

            count = 0.0;


            for (EarningsAgeCount val : values) {
                sumEarnings += val.earnings.get();
                sumAge += val.age.get();
                count += val.count.get();
            }

            avgAge = sumAge/count;
            avgEarnings = sumEarnings/count;


            resultValue.set(avgEarnings+ "\t"+avgAge +"\t"+count);
            context.write(key,resultValue);
        }
    }

    public static class CustomCombiner extends Reducer<IntWritable, EarningsAgeCount, IntWritable, EarningsAgeCount> {
        private final EarningsAgeCount resultValue = new EarningsAgeCount(0.0,0,0);

        public void reduce(IntWritable key, Iterable<EarningsAgeCount> values, Context context) throws IOException, InterruptedException {
            for (EarningsAgeCount val : values) {
                resultValue.addEarningsAgeCount(val);
            }
            context.write(key, resultValue);
        }
    }

}