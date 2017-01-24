import { Component, OnInit, AfterViewInit, ElementRef, ViewChild, Input } from '@angular/core';

import { QuestionService } from '../../services/question.service';

const SimpleMDE: any = require('simplemde');

@Component({
  selector: 'app-markdown',
  templateUrl: './markdown.component.html',
  styleUrls: ['./markdown.component.less']
})
export class MarkdownComponent implements OnInit, AfterViewInit {
  @ViewChild('simplemde') textarea: ElementRef;
  @Input() raw: string;
  mde: any;

  constructor(
    private elementRef: ElementRef,
    private questionService: QuestionService) { }

  getValue(): string {
    return this.mde.value();
  }

  ngOnInit() {
  }

  ngAfterViewInit() {
    this.mde = new SimpleMDE({
      element: this.elementRef.nativeElement.value,
      showIcons: ['code', 'table'],
      autoDownloadFontAwesome: false,
      spellChecker: false
    });
  }

}
