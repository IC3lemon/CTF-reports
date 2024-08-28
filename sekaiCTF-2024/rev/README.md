# CrackMe

given is a react native .apk \
Using apktool, we can extract `index.android.bundle` from the apk \
and putting this into `react-native-decompiler`gives out the js files inside \
and there were about 600 js files. \
Akash and Harshit went through those to find this ting \
```js
var _ = {
  LOGIN: 'LOGIN',
  EMAIL_PLACEHOLDER: 'user@sekai.team',
  PASSWORD_PLACEHOLDER: 'password',
  BEGIN: 'CRACKME',
  SIGNUP: 'SIGN UP',
  LOGOUT: 'LOGOUT',
  KEY: 'react_native_expo_version_47.0.0',
  IV: '__sekaictf2023__',
};
exports.default = _;
```

the `key` and `iv` hinted that this could be aes. \
and ye it was aes. \
The app was a login thingy. So that meant the password was being validated. prolly using aes. \
and yes there was a validation function 
```js
e.validatePassword = function (e) {
      if (17 !== e.length) return false;
      var t = module700.default.enc.Utf8.parse(module456.default.KEY),
        n = module700.default.enc.Utf8.parse(module456.default.IV);
      return (
        '03afaa672ff078c63d5bdb0ea08be12b09ea53ea822cd2acef36da5b279b9524' ===
        module700.default.AES.encrypt(e, t, {
          iv: n,
        }).ciphertext.toString(module700.default.enc.Hex)
      );
    };
```

So we have `ct = 03afaa672ff078c63d5bdb0ea08be12b09ea53ea822cd2acef36da5b279b9524` \
we got `iv` and `key` also. \
boom `s3cr3t_SEKAI_P@ss` \
Got the password for the ting. 

Then logged into the thing as admin using this password and the user as \
`user@sekai.team`

Now what Akash and Harshith did was, they logged in with these credentials \
attached `HTTP Toolkit` and logged all the network requests. \
and in one GET request they found it.

`SEKAI{15_React_N@71v3_R3v3rs3_H@RD???}`

The intended solve was \
go to the firebase db where all the user ids were hashed and stored \
and then run a script to bruteforce through all the hashes.


## Takeaways 
- learnt about react-native-decompiler
- learnt about apktools
- learnt about HTTP toolkit