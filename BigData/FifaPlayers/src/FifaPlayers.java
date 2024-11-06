import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

public class FifaPlayers extends Configured implements Tool {

    public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new FifaPlayers(), args);
        System.exit(res);
    }

    public int run(String[] args) throws Exception {
        Job job = Job.getInstance(getConf(), "FifaPlayers");
        job.setJarByClass(this.getClass());
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.setMapperClass(FifaPlayersMapper.class);
        job.setReducerClass(FifaPlayersReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(PlayerData.class);

        // Increase memory allocation
        job.getConfiguration().set("mapreduce.map.memory.mb", "2048");
        job.getConfiguration().set("mapreduce.reduce.memory.mb", "4096");

        // Increase timeout settings
        job.getConfiguration().set("mapreduce.task.timeout", "600000");

        boolean jobCompleted = job.waitForCompletion(true);
        if (!jobCompleted) {
            System.err.println("Job failed. Check logs for details.");
        }
        return jobCompleted ? 0 : 1;
    }

    public static class FifaPlayersMapper extends Mapper<LongWritable, Text, Text, PlayerData> {
        private final Text league = new Text();
        private final SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        private int calculateAge(String birthdateStr) throws Exception {
            Date birthdate = dateFormat.parse(birthdateStr);
            Calendar current = Calendar.getInstance();
            Calendar birth = Calendar.getInstance();
            birth.setTime(birthdate);
            int age = current.get(Calendar.YEAR) - birth.get(Calendar.YEAR);
            if (current.get(Calendar.DAY_OF_YEAR) < birth.get(Calendar.DAY_OF_YEAR)) {
                age--;
            }
            return age;
        }

        public void map(LongWritable offset, Text lineText, Context context) {
            try {
                String line = lineText.toString();
                String[] fields = line.split(";");
                String leagueId = fields[16];
                String birthDate = fields[13];
                String wage = fields[11];
                String weightStr = fields[15];
                int weight = Integer.parseInt(weightStr);

                int age = calculateAge(birthDate);
                if (weight >= 100 || wage == null || wage.isEmpty() || wage.equals("null")) {
                    return;
                }
                double wageValue = Double.parseDouble(wage);
                league.set(leagueId);
                context.write(league, new PlayerData(age, wageValue));
            } catch (Exception e) {
                e.printStackTrace();
                System.err.println("Error processing line: " + lineText.toString());
            }
        }
    }

    public static class FifaPlayersReducer extends Reducer<Text, PlayerData, Text, Text> {
        private final Text resultValue = new Text();
        @Override
        public void reduce(Text key, Iterable<PlayerData> values, Context context) throws IOException, InterruptedException {
            try {
                double totalAge = 0;
                double totalWage = 0;
                int playerCount = 0;
                for (PlayerData val : values) {
                    totalAge += val.getAge();
                    totalWage += val.getWage();
                    playerCount++;
                }
                if (playerCount > 0) {
                    double averageAge = totalAge / playerCount;
                    double averageWage = totalWage / playerCount;
                    String resultString = String.format(Locale.US, "%.2f;%.2f;%d", averageAge, averageWage, playerCount);
                    resultValue.set(resultString);
                    context.write(new Text(key.toString() + ";"), resultValue); // Key and value separated by ;
                } else {
                    System.err.println("No valid players for league: " + key.toString());
                }
            } catch (Exception e) {
                e.printStackTrace();
                System.err.println("Error reducing key: " + key.toString());
            }
        }
    }

    public static class PlayerData implements Writable {
        private int age;
        private double wage;

        public PlayerData() {}

        public PlayerData(int age, double wage) {
            this.age = age;
            this.wage = wage;
        }

        public int getAge() {
            return age;
        }

        public double getWage() {
            return wage;
        }

        @Override
        public void write(DataOutput out) throws IOException {
            out.writeInt(age);
            out.writeDouble(wage);
        }

        @Override
        public void readFields(DataInput in) throws IOException {
            age = in.readInt();
            wage = in.readDouble();
        }

        @Override
        public String toString() {
            return age + "`" + wage;
        }
    }
}