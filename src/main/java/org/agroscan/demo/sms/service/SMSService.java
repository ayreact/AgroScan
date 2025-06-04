package org.agroscan.demo.sms.service;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.twilio.twiml.MessagingResponse;
import com.twilio.twiml.messaging.Body;
import com.twilio.twiml.messaging.Media;
import com.twilio.twiml.messaging.Message;
import org.agroscan.demo.sms.response.DataResponse;
import org.agroscan.demo.sms.response.ErrorResponse;
import org.agroscan.demo.sms.response.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.twilio.type.PhoneNumber;
import com.twilio.Twilio;
import org.agroscan.demo.sms.model.*;

import java.awt.image.BufferedImage;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.*;

import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import javax.imageio.ImageIO;

@Service
public class SMSService {


      @Value("${agroscan-account-sid}")
      private String ACCOUNT_SID;  
      @Value("${agroscan-auth-token}")
      private String AUTH_TOKEN;
      @Value("${agroscan-dev-num}")
      private String DEV_NUM;
      @Value("${diagnosis-key}")
      private String dkey;

      @Autowired
      private RestTemplate restTemplate;
      private ObjectMapper objectMapper = new ObjectMapper();
      private String path = System.getProperty("java.io.tmpdir");
      private Logger logger = LoggerFactory.getLogger(SMSService.class);
      private String url = "https://agroscan-xasy.onrender.com/new-chat/sms-diagnosis";


    public String sendSMS(Integer numMedia,String ...data)  {
        try {
            Twilio.init(ACCOUNT_SID, AUTH_TOKEN);
            System.out.println("authenticated.....");
            String from = data[0];
            String body = data[1];
            String mediaUrl = data[2];
            ApiData apiData = new ApiData();
            apiData.setBody(body);
            apiData.setFrom(from);
            apiData.setMediaUrl0(mediaUrl);
            apiData.setNumMedia(numMedia.intValue());

            if (!Objects.isNull(mediaUrl)) {
                apiData.setImage(getFilefromUrl(mediaUrl));
                com.twilio.rest.api.v2010.account.Message message =
                        com.twilio.rest.api.v2010.account.Message.creator(
                                        new PhoneNumber(from),
                                        new PhoneNumber(DEV_NUM),
                                        extractData(Objects.requireNonNull(readApi(apiData))).substring(0,147)
                                )
                                .setMediaUrl(new URI(mediaUrl))
                                .create();
            } else {
                com.twilio.rest.api.v2010.account.Message message =
                        com.twilio.rest.api.v2010.account.Message.creator(
                                new PhoneNumber(from),
                                new PhoneNumber(DEV_NUM),
                                extractData(Objects.requireNonNull(readApi(apiData))).substring(0,147)
                        ).create();
            }
        }
        catch(URISyntaxException e) {
            return e.getMessage();
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
        return "";
    }

    public String sendPlainText(String format) {
        Body responseBody = new Body.Builder(format).build();
        var message = new Message.Builder()
                .body(responseBody)
                .build();

        MessagingResponse twiml = new MessagingResponse.Builder()
                .message(message)
                .build();

        return twiml.toXml();

    }

    public String extractData(Response response) {
        DataResponse dataResponse = response.getData();
        String format = "";
        if(!Objects.isNull(dataResponse)) {
             format = "\n\n\nDiagnosis Title: " + dataResponse.getDiagnosis_title() +
                    "\n\n\nHealth Condition: " + dataResponse.getHealth_condition() +
                    "\n\n\nCause: " + dataResponse.getCause() +
                    "\n\n\nControl: " + dataResponse.getControl_suggestions() +
                    "\n\n\nDisease Signs: " + dataResponse.getDisease_signs() +
                    "\n\n\nSummary: " + dataResponse.getSummary();
        }
        else {
            format = response.getError();
        }

        return format;
    }

    public void sendWhatsappMessage(Integer numMedia,String ...data) throws JsonProcessingException {
          Twilio.init(ACCOUNT_SID,AUTH_TOKEN);
          ApiData apiData = new ApiData();
          apiData.setBody(data[1]);
          apiData.setFrom(data[0]);
          System.out.println(data[2]);
              if (data[2] != null) {
                  System.out.println("with whatsapp");
                  File outputFile = getFilefromUrl(data[2]);
                  if (!Objects.isNull(outputFile)) {
                      System.out.println("From: " + data[0]);
                      apiData.setImage(outputFile);
                      sendMessageWithTwilio(data[0], extractData(Objects.requireNonNull(readApi(apiData))));
                  }
              } else {
                  System.out.println("without whatsapp");
                  sendMessageWithTwilio(data[0], extractData(Objects.requireNonNull(readApi(apiData))));
              }
    }

    public void sendMessageWithTwilio(String to, String data) {
        com.twilio.rest.api.v2010.account.Message message = com.twilio.rest.api.v2010.account.Message.creator(
                new PhoneNumber(to),
                new PhoneNumber("whatsapp:+14155238886"),
                data
        ).create();
    }


    public File getFilefromUrl(String url) {
            String msg = "";
          try {
              URL objUrl = new URL(url);
              HttpURLConnection connection = (HttpURLConnection) objUrl.openConnection();

              String credentials = ACCOUNT_SID+":"+AUTH_TOKEN;
              String basicAuth = "Basic "+Base64.getEncoder().encodeToString(credentials.getBytes());

              connection.setRequestProperty("Authorization",basicAuth);
              InputStream is = connection.getInputStream();
              BufferedImage bufferedImage = ImageIO.read(is);

              if(bufferedImage != null) {
                  File outputFile = new File(path,"test.jpg");
                  ImageIO.write(bufferedImage,"jpg",outputFile);
                  return outputFile;
              }
          }
          catch(Exception e) {
              System.out.println(e.getMessage());
          }
          return null;
    }

    private Response readApi(ApiData apiData) throws JsonProcessingException {
        Response data = new Response();
        try {
            File file = apiData.getImage();
            FileSystemResource fileResource = null;
            if (file != null) {
                fileResource = new FileSystemResource(file);
            }

            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("text", apiData.getBody());
            if (fileResource != null) {
                body.add("image", fileResource);
            }

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);
            headers.set("Diagnosis-Key", dkey);

            HttpEntity<MultiValueMap<String, Object>> requestEntity =
                    new HttpEntity<>(body, headers);
            ResponseEntity<Response> response = restTemplate
                    .postForEntity(url, requestEntity, Response.class);
            System.out.println(response.getBody().toString());
            return response.getBody();

        } catch (Exception e) {
            String json = e.getMessage().substring(17);
            data.setError(json);
            return data;
        }
    }
}