import { Component, OnInit, ElementRef, Renderer2 } from '@angular/core';
import { HttpClient,HttpHeaders } from '@angular/common/http';
import { AuthService } from 'auth.service';
@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit {
  constructor(private elementRef: ElementRef, private renderer: Renderer2, private http: HttpClient, private authService:AuthService) { }
  ngOnInit(): void {
    this.setupCollapsible();
    this.firstBotMessage();
  }
  setupCollapsible(): void {
    const collapsibleButtons = Array.from(this.elementRef.nativeElement.getElementsByClassName('collapsible')) as HTMLElement[];
    collapsibleButtons.forEach((button: HTMLElement) => {
      button.addEventListener('click', () => {
        button.classList.toggle('active');
        const content = button.nextElementSibling as HTMLElement | null;
        if (content?.style.maxHeight) {
          content.style.maxHeight = '';
        } else if (content) {
          content.style.maxHeight = content.scrollHeight + 'px';
        }
      });
    });
  }
  getTime(): string {
    const today = new Date();
    let hours: string | number = today.getHours();
    let minutes: string | number = today.getMinutes();

    if (hours < 10) {
      hours = "0" + hours;
    }

    if (minutes < 10) {
      minutes = "0" + minutes;
    }

    const time = hours + ":" + minutes;
    return time;
  }

  firstBotMessage(): void {
    const botStarterMessage = this.elementRef.nativeElement.querySelector('#botStarterMessage');
    if (botStarterMessage) {
      const botText = this.renderer.createElement('p');
      this.renderer.addClass(botText, 'botText');
      const span = this.renderer.createElement('span');
      this.renderer.appendChild(span, this.renderer.createText("How's it going?"));
      this.renderer.appendChild(botText, span);
      this.renderer.appendChild(botStarterMessage, botText);
    }
    const chatTimestamp = this.elementRef.nativeElement.querySelector('#chat-timestamp');
    if (chatTimestamp) {
      chatTimestamp.innerHTML = this.getTime();
    }
    const userInput = this.elementRef.nativeElement.querySelector('#userInput');
    if (userInput) {
      userInput.scrollIntoView(false);
    }
  }

  getHardResponse(userText: string): void {
    const apiUrl = 'http://127.0.0.1:5000/answer'
    const token = this.authService.getToken();
    const headers = new HttpHeaders({
      'Content-Type':'application/json',
      Authorization: `Bearer ${token}`
    });
    this.http.post(apiUrl, { question: userText },{headers:headers}).subscribe((response: any) => {
      const botResponse = response.answer;
      const chatbox = this.elementRef.nativeElement.querySelector('#chatbox');
      if (chatbox) {
        const botText = this.renderer.createElement('p');
        this.renderer.addClass(botText, 'botText');
        const span = this.renderer.createElement('span');
        this.renderer.appendChild(span, this.renderer.createText(botResponse));
        this.renderer.appendChild(botText, span);
        this.renderer.appendChild(chatbox, botText);
      }
  
      const chatBarBottom = this.elementRef.nativeElement.querySelector('#chat-bar-bottom');
      if (chatBarBottom) {
        chatBarBottom.scrollIntoView(true);
      }
    });
  }
  
  

  getResponse(): void {
    let userText = (<HTMLInputElement>this.elementRef.nativeElement.querySelector("#textInput")).value;
    if (userText === "") {
      userText = "Thanks for your response❤️";
    }
    (<HTMLInputElement>this.elementRef.nativeElement.querySelector("#textInput")).value = "";
    const chatbox = this.elementRef.nativeElement.querySelector("#chatbox");
    if (chatbox) {
      const userTextElement = this.renderer.createElement('p');
      this.renderer.addClass(userTextElement, 'userText');
      const span = this.renderer.createElement('span');
      this.renderer.appendChild(span, this.renderer.createText(userText));
      this.renderer.appendChild(userTextElement, span);
      this.renderer.appendChild(chatbox, userTextElement);
    }
    const chatBarBottom = this.elementRef.nativeElement.querySelector("#chat-bar-bottom");
    if (chatBarBottom) {
      chatBarBottom.scrollIntoView(true);
    }
  
    setTimeout(() => {
      this.getHardResponse(userText);
    }, 1000);
  }
  

  buttonSendText(sampleText: string): void {
    (<HTMLInputElement>this.elementRef.nativeElement.querySelector("#textInput")).value = "";
    const chatbox = this.elementRef.nativeElement.querySelector("#chatbox");
    if (chatbox) {
      const userTextElement = this.renderer.createElement('p');
      this.renderer.addClass(userTextElement, 'userText');
      const span = this.renderer.createElement('span');
      this.renderer.appendChild(span, this.renderer.createText(sampleText));
      this.renderer.appendChild(userTextElement, span);
      this.renderer.appendChild(chatbox, userTextElement);
    }
    const chatBarBottom = this.elementRef.nativeElement.querySelector("#chat-bar-bottom");
    if (chatBarBottom) {
      chatBarBottom.scrollIntoView(true);
    }
  }
  

  sendButton(): void {
    this.getResponse();
  }

  heartButton(): void {
    this.buttonSendText("Heart clicked!");
  }

  onKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      this.getResponse();
    }
  }
}
