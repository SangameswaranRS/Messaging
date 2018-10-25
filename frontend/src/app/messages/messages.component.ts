import { Component, OnInit } from '@angular/core';
import {HttpHeaders, HttpClient} from '@angular/common/http';
import {CookieService} from 'ngx-cookie-service';
import { RouterModule, Routes, Router } from '@angular/router';


@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.scss']
})
export class MessagesComponent implements OnInit {

  http: any;
  cookie: any;
  API_BASE_URL = 'http://localhost:5959';
  messagesJson = [];
  userJson = [];
  selectedDestinationUID: any;
  messageEntered: any;
  route: any;

  constructor(httpClient: HttpClient, cookie: CookieService, route: Router) {
    this.http = httpClient;
    this.cookie = cookie;
    this.route = route;
  }

  ngOnInit() {
    const uid = this.cookie.get('uid');
    console.log(uid);
    if (uid === '') {
      this.route.navigate(['login']);
    }
    const headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8')
                                      .set('uid', uid);
    const options = {
      headers: headers
    };
    this.http.get(this.API_BASE_URL + '/user/getMessages', options).toPromise().then(
      success => {
          this.messagesJson = success.message;
      },
      error => {
        console.log(error);
        alert('Something went wrong');
      }
    );
    this.http.get(this.API_BASE_URL + '/user/getUserData', options).toPromise().then(
      success => {
          this.userJson = success.message;
      },
      error => {
        console.log(error);
        alert('Failed to retreive user list');
      }
    );
  }
  message() {
    const uid = this.cookie.get('uid');
    const headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8')
                                      .set('uid', uid);
    const options = {
      headers: headers
    };
    const postparams = {
      destinationUserId: this.selectedDestinationUID,
      message: this.messageEntered
    };
    this.http.post(this.API_BASE_URL + '/user/sendMessage', postparams, options).toPromise().then(
      success => {
        alert(success.message);
      },
      error => {
        console.log(error);
        alert(error.error.message);
      }
    );
  }

  logout() {
    this.cookie.set('uid', '');
    this.route.navigate(['login']);
  }

}
