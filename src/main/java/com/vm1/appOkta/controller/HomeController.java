package com.vm1.appOkta.controller;

import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.oidc.user.OidcUser;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HomeController {
    
/*     @GetMapping("/")
    public String index() {
        return "App is running. Try accessing /home for Okta login.";
    } */

    @GetMapping("/login")
    public String login() {
        return "Login page";
    }
    
    @GetMapping("/") 
    public String home(@AuthenticationPrincipal OidcUser user) {
        if (user == null) return "Error: No authenticated user found";
        return "Welcome, "+ user.getFullName() + "!";
    }

}
