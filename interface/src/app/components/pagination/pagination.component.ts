import { Component, OnInit, OnChanges, Input } from '@angular/core';
import { UrlSerializer, UrlTree, Params } from '@angular/router';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.less']
})
export class PaginationComponent implements OnInit, OnChanges {
  @Input() next: string;
  @Input() prev: string;
  @Input() url: string;

  nextUrlParams: Params;
  prevUrlParams: Params;

  constructor(
    private urlSerializer: UrlSerializer
  ) {
  }

  ngOnInit() {
  }

  ngOnChanges() {
    this.nextUrlParams = this.urlSerializer.parse(this.next || '').queryParams;
    this.prevUrlParams = this.urlSerializer.parse(this.prev || '').queryParams;
  }

}
