import { Component, OnInit } from '@angular/core';
import {HttpHeaders, HttpClient} from '@angular/common/http';
import {CookieService} from 'ngx-cookie-service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  cookie: any;
  router: any;
  http: any;
  username: any;
  password: any;
  API_BASE_URL = 'http://localhost:5959';
  constructor(httpClient: HttpClient, cookie: CookieService, router: Router) {
    this.http = httpClient;
    this.cookie = cookie;
    this.router = router;
  }

  ngOnInit() {
  }

  login() {
    const headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8');
    const options =  {
      headers: headers
    };
    const postParams = {
      username: this.username,
      password: this.password
    };
    this.http.post(this.API_BASE_URL + '/user/login', postParams, options).toPromise().then(
      success => {
        console.log(success);
        alert(success.message);
        this.cookie.set('uid', success.userId);
        this.router.navigate(['messages']);
      },
      error => {
        console.log(error);
        alert(error.error.message);
      }
    );
  }

  signup() {
    this.router.navigate(['signup']);
  }

}
