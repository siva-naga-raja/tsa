package com.b2b.task.assignment;

import com.b2b.task.assignment.BO.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.Arrays;

@RestController
public class Controller {
    @Autowired
    Service service;

    @GetMapping("/tasks")
    @ResponseBody
    public String getNTasks() throws IOException, InterruptedException {
        return service.getNTasks();
    }

    @PostMapping("/email")
    @ResponseBody
    public String sendEmail(@RequestBody String assignmentData) throws Exception {
        boolean mailStatus = service.sendEmail(assignmentData);
        if (mailStatus) { return "{\"response\": " + "\"mail sent successfully\"}"; }
        return "{\"response\": " + "\"error in sending mail\"}";
    }

    @PostMapping("/assign")
    @ResponseBody
    public String assignTasks(@RequestBody AssignableMember[] assignableMembers) throws Exception {
        return service.assignTasks(Arrays.toString(assignableMembers));
    }

}
