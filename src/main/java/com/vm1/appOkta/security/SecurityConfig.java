package com.vm1.appOkta.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
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
            // Configuración de login con OAuth2 (Okta)
            .oauth2Login(oauth2 -> oauth2
                .redirectionEndpoint(redir -> redir
                    .baseUri("/login/oauth2/code")
                )
            );
/*             // Configuración de logout
            .logout(logout -> logout
                .logoutSuccessUrl("/") // Redirige a la página principal tras logout
                .invalidateHttpSession(true) // Invalida la sesión HTTP
                .clearAuthentication(true) // Limpia la autenticación
            ); */

        return http.build();
    }
}
