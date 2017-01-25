import { Component, OnInit } from '@angular/core';

import { VERSION } from '../../../environments/const';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.less']
})
export class FooterComponent implements OnInit {
  version: string;

  constructor() {
    this.version = VERSION;
  }

  ngOnInit() {
  }

}
