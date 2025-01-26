package com.vm1.appOkta.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
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
            .oauth2Client(Customizer.withDefaults());


        return http.build();
    }
}
