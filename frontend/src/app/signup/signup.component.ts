import { Component } from '@angular/core';
import { AuthService } from 'auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  name: string = '';
  email: string = '';
  password: string = '';

  constructor(private authService: AuthService) { }

  signup() {
    this.authService.signup(this.name, this.email, this.password).subscribe(
      (response) => {
        alert("Registered Successfully")
        console.log(response);
      },
      (error) => {
        console.error(error);
      }
    );
  }
}
