package com.vm1.appOkta.security;

import java.util.Map;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.client.OAuth2AuthorizationSuccessHandler;
import org.springframework.security.oauth2.client.OAuth2AuthorizedClient;
import org.springframework.security.oauth2.client.OAuth2AuthorizedClientManager;
import org.springframework.security.oauth2.client.registration.ClientRegistrationRepository;
import org.springframework.security.oauth2.client.web.DefaultOAuth2AuthorizedClientManager;
import org.springframework.security.oauth2.client.web.OAuth2AuthorizedClientRepository;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            // Configuración de autorización
            .authorizeHttpRequests(authorize -> authorize
                .requestMatchers("/public/**").permitAll() // Rutas públicas sin autenticación
                .anyRequest().authenticated() // Cualquier otra ruta requiere autenticación
            )
            .oauth2Login(oauth2 -> oauth2
                .defaultSuccessUrl("/home", true) // Redirige a /home tras login exitoso
                .redirectionEndpoint(endpoint -> endpoint
                    .baseUri("/login/oauth2/code/okta")
                )   
            )
            .oauth2Client(Customizer.withDefaults())
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED) // Configura una sesión si es necesaria
            );


        return http.build();
    }

    @Bean
    public OAuth2AuthorizedClientManager authorizedClientManager(
            ClientRegistrationRepository clientRegistrationRepository,
            OAuth2AuthorizedClientRepository authorizedClientRepository) {

        DefaultOAuth2AuthorizedClientManager authorizedClientManager =
                new DefaultOAuth2AuthorizedClientManager(clientRegistrationRepository, authorizedClientRepository);

        // Configura un manejador de éxito personalizado
        authorizedClientManager.setAuthorizationSuccessHandler(new OAuth2AuthorizationSuccessHandler() {
            @Override
            public void onAuthorizationSuccess(OAuth2AuthorizedClient authorizedClient,
                                               Authentication principal,
                                               Map<String, Object> attributes) {
                // Establece el contexto de seguridad aquí
                SecurityContextHolder.getContext().setAuthentication(principal);
                System.out.println("Autenticación exitosa para el cliente: " + authorizedClient.getClientRegistration().getClientId());
            }
        });

        return authorizedClientManager;
    }

}
