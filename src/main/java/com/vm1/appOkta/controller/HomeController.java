package com.vm1.appOkta.controller;

import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.client.web.HttpSessionOAuth2AuthorizationRequestRepository;
import org.springframework.security.oauth2.core.endpoint.OAuth2AuthorizationRequest;
import org.springframework.security.oauth2.core.oidc.user.OidcUser;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.UriComponentsBuilder;

import jakarta.servlet.http.HttpServletRequest;

@RestController
public class HomeController {
    
/*     @GetMapping("/")
    public String index() {
        return "App is running. Try accessing /home for Okta login.";
    } */
   @GetMapping("/login")
    public String login(HttpServletRequest request) {
        OAuth2AuthorizationRequest authorizationRequest = (OAuth2AuthorizationRequest) request.getSession()
            .getAttribute(HttpSessionOAuth2AuthorizationRequestRepository.class.getName() + ".AUTHORIZATION_REQUEST");

        if (authorizationRequest != null) {
            String authorizationUri = UriComponentsBuilder.fromUriString(authorizationRequest.getAuthorizationUri())
                .queryParam("client_id", authorizationRequest.getClientId())
                .queryParam("redirect_uri", authorizationRequest.getRedirectUri())
                .queryParam("response_type", authorizationRequest.getResponseType().getValue())
                .queryParam("scope", String.join(" ", authorizationRequest.getScopes()))
                .queryParam("state", authorizationRequest.getState())
                .build().toUriString();

            System.out.println("Authorization URI: " + authorizationUri);
        }

        return "Login page";
    }

    @GetMapping("/home") 
    public String home(@AuthenticationPrincipal OidcUser user) {
        if (user == null) return "Error: No authenticated user found";
        return "Welcome, "+ user.getFullName() + "!";
    }

}
