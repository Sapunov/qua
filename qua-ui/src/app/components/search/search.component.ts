import { Component, OnInit, Input } from '@angular/core';
import { Router, NavigationExtras, ActivatedRoute, Params } from '@angular/router';

import { MIN_CHARS_FOR_SEARCH } from '../../../environments/const';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.less']
})
export class SearchComponent implements OnInit {
  @Input() sfHide: boolean;
  query: string;
  timer: number;

  constructor(
    private router: Router,
    private route: ActivatedRoute) {
    this.query = '';
    }


  getResults(query: string) {
    if (!query || this.query.length < MIN_CHARS_FOR_SEARCH) {
      return;
    }
    let params: NavigationExtras = {
      queryParams: {
        query: query
      }
    };
    this.router.navigate(['/search'], params);
  }

  keyup(event: KeyboardEvent) {
    if (this.query.length < MIN_CHARS_FOR_SEARCH) {
      return;
    }
    if (event.code === 'Enter' || event.key === 'Enter' || event.which === 13) {
      clearTimeout(this.timer);
      return;
    }
    if (this.timer) {
      clearTimeout(this.timer);
    }
    this.timer = window.setTimeout(() => {
      this.getResults(this.query);
    }, 300);
  }

  ngOnInit() {
    this.route.queryParams.subscribe((param: Params) => {
      this.query = param['query'] || '';
    });
  }
}
