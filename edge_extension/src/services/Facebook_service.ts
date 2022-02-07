import config from './config';

function initFB() {
    return new Promise(resolve => {
        // wait for facebook sdk to initialize before starting the react app
        window.fbAsyncInit = function () {
            window.FB.init({
                appId: config.CLIENT_ID_FB,
                cookie: true,
                xfbml: true,
                version: '12.0'
            });

            // auto authenticate with the api if already logged in with facebook
            // window.FB.getLoginStatus(({ authResponse }) => {
            //     if (authResponse) {
            //         accountService.apiAuthenticate(authResponse.accessToken).then(resolve);
            //     } else {
            //         resolve();
            //     }
            // });
        };

        // load facebook sdk script
        (function (d: any, s: any, id: any) {
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) { return; }
            js = d.createElement(s); js.id = id;
            js.src = "https://connect.facebook.net/en_US/sdk.js";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
    });
};