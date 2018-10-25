import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import {HttpHeaders, HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnInit {
  router: any;
  http: any;
  username: any;
  password: any;
  emailid: any;
  API_BASE_URL = 'http://localhost:5959';
  constructor(r: Router, http: HttpClient) {
    this.router = r;
    this.http = http;
   }

  ngOnInit() {
  }

  signup() {
    console.log(this.http);
    const headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8');
    const options =  {
      headers: headers
    };
    const postparams = {
      username: this.username,
      password: this.password,
      emailid: this.emailid
    };
    this.http.get(this.API_BASE_URL + '/user/getUserData').toPromise();
    this.http.post(this.API_BASE_URL + '/user/signup', postparams, options).toPromise().then(
      success => {
        console.log(success);
        alert('Signup Successful!');
        this.router.navigate(['login']);
      },
      error => {
        console.log(error);
        alert('Signup Failed');
      }
    );

  }

}
