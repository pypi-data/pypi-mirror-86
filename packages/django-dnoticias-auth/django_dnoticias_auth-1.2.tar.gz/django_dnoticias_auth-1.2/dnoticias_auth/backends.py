from mozilla_django_oidc.auth import OIDCAuthenticationBackend
import logging

logger = logging.getLogger(__name__)

class ExtraClaimsOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        """Return object for a newly created user account."""
        
        email = claims.get('email')
        first_name = claims.get("given_name", None)
        last_name = claims.get("family_name", None)
        is_staff = claims.get("is_staff", False)

        username = self.get_username(claims)

        return self.UserModel.objects.create_user(username, email, first_name=first_name, last_name=last_name, is_staff=is_staff)
    
    def update_user(self, user, claims):
        has_changes = False

        email = claims.get('email')
        first_name = claims.get("given_name", None)
        last_name = claims.get("family_name", None)
        is_staff = claims.get("is_staff", False)
        
        if user.email != email:
            logger.info("Updating user email...")
            user.email = email
            has_changes = True
        
        if user.first_name != first_name:
            logger.info("Updating user first_name...")
            user.first_name = first_name
            has_changes = True
        
        if user.last_name != last_name:
            logger.info("Updating user last_name...")
            user.last_name = last_name
            has_changes = True
        
        if user.is_staff != is_staff:
            logger.info("Updating user staff status...")
            user.is_staff = is_staff
            has_changes = True
        
        if has_changes:
            user.save()

        return user