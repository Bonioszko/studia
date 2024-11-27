package com.example.bigdata;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.WritableComparable;

import java.io.*;

public class EarningsAgeCount implements WritableComparable<EarningsAgeCount> {

    DoubleWritable earnings;
    IntWritable age;
    IntWritable count;

    public EarningsAgeCount() {
        set(new DoubleWritable(0), new IntWritable(0), new IntWritable(0));
    }

    public EarningsAgeCount(Double earnings, Integer age, Integer count) {
        set(new DoubleWritable(earnings), new IntWritable(age) ,new IntWritable(count));
    }

    public void set(DoubleWritable earnings,  IntWritable age ,IntWritable count) {
        this.earnings = earnings;
        this.age = age;
        this.count = count;
    }

    public DoubleWritable getEarnings() {
        return earnings;
    }

    public IntWritable getCount() {
        return count;
    }
    public IntWritable getAge() {
        return age;
    }

    public void addEarningsAgeCount(EarningsAgeCount earningsAgeCount) {
        set(new DoubleWritable(this.earnings.get() + earningsAgeCount.getEarnings().get()),new IntWritable(this.age.get() + earningsAgeCount.getAge().get()) ,new IntWritable(this.count.get() + earningsAgeCount.getCount().get()));
    }

    @Override
    public void write(DataOutput dataOutput) throws IOException {
        earnings.write(dataOutput);
        age.write(dataOutput);
        count.write(dataOutput);
    }

    @Override
    public void readFields(DataInput dataInput) throws IOException {
        earnings.readFields(dataInput);
        age.readFields(dataInput);
        count.readFields(dataInput);
    }

    // Do poprawy najpewniej
    @Override
    public int compareTo(EarningsAgeCount earningsAgeCount) {

        int cmp = earnings.compareTo(earningsAgeCount.earnings);
        if (cmp != 0) {
            return cmp;
        }

        cmp = age.compareTo(earningsAgeCount.age);
        if (cmp != 0) {
            return cmp;
        }

        return count.compareTo(earningsAgeCount.count);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        EarningsAgeCount earningsAgeCount = (EarningsAgeCount) o;

        return count.equals(earningsAgeCount.count) && earnings.equals(earningsAgeCount.earnings) && age.equals(earningsAgeCount.age) ;

    @Override
    public int hashCode() {
        int result = earnings.hashCode();
        result = 31 * result + count.hashCode();
        return result;
    }
}