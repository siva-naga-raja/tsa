package com.b2b.task.assignment;

import javax.mail.*;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMultipart;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Properties;
import java.util.StringTokenizer;

@org.springframework.stereotype.Service
public class Service {
    public static final String EMAIL_HOST = "<enter your details>";
    public static final String EMAIL_USERNAME = "<enter your details>";
    public static final String EMAIL_PASSWORD = "<enter your details>";
    public static final String EMAIL_FROM = "<enter your details>";
    public static final String EMAIL_TO = "<enter your details>";
    public static final String EMAIL_CC = "<enter your details>";
    public static final String EMAIL_SUBJECT = "<enter your details>";

    public String assignTasks(String jsonData) throws Exception {
        String[] command = {"python", "<absolute_path_to_the_python_script_file>", jsonData};
        Process process = new ProcessBuilder(command).start();
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        StringBuilder output = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            output.append(line).append("\n");
        }
        process.waitFor();

        String outputStr = output.toString();
        boolean emailStatus = sendEmail(outputStr);

        if (emailStatus) { return "{\"status\": \"success\", \"emailResponse\": \"" + outputStr + "\"}"; }
        return "{\"status\": \"failure\", \"emailResponse\": \"" + outputStr + "\"}";
    }

    public String getNTasks() throws IOException, InterruptedException {
        String[] command = {"python", "<absolute_path_to_the_python_script_file>"};
        Process process = new ProcessBuilder(command).start();
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        StringBuilder output = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            output.append(line).append("\n");
        }
        process.waitFor();
        String outputStr = output.toString();
        return outputStr;
    }

    public boolean sendEmail(String assignmentData) throws Exception {
        Properties props = new Properties();
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");
        props.put("mail.smtp.host", EMAIL_HOST);
        props.put("mail.smtp.port", "25");
        props.put("mail.smtp.starttls.required", "false");
        props.put("test-connection", "false");

        Session session = Session.getInstance(props,
                new javax.mail.Authenticator() {
                    protected PasswordAuthentication getPasswordAuthentication() {
                        return new PasswordAuthentication(EMAIL_USERNAME, EMAIL_PASSWORD);
                    }
                });

        try {

            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress(EMAIL_FROM));

            StringTokenizer localStringTokenizer = null;
            if (EMAIL_TO != null && EMAIL_TO.length() > 0) {
                localStringTokenizer = new StringTokenizer(EMAIL_TO, ";");
            }

            if(localStringTokenizer!=null){
                while (localStringTokenizer.hasMoreTokens()) {
                    message.addRecipient(Message.RecipientType.TO,
                            new InternetAddress(localStringTokenizer.nextToken()));
                }
            }

            localStringTokenizer = null;
            if (EMAIL_CC != null && EMAIL_CC.length() > 0) {
                localStringTokenizer = new StringTokenizer(EMAIL_CC, ";");
            }

            if(localStringTokenizer!=null){
                while (localStringTokenizer.hasMoreTokens()) {
                    message.addRecipient(Message.RecipientType.CC,
                            new InternetAddress(localStringTokenizer.nextToken()));
                }
            }

            MimeMultipart mimeMultipart = new MimeMultipart("related");

            BodyPart mimeBodyPart = new MimeBodyPart();
            String body = "Hi Team, <br><br>Please find below, task assignment for the day<br><br>" + assignmentData + "<br>Thanks,<br>B2B OM.";
            mimeBodyPart.setContent(body, "text/html");

            mimeMultipart.addBodyPart(mimeBodyPart);

            message.setContent(mimeMultipart);
            message.setSubject(EMAIL_SUBJECT + getDate());

            Transport.send(message);
            return true;
        } catch (Exception e) {
            System.out.println("*****Exception in sending email*****");
            return false;
        }
    }

}
