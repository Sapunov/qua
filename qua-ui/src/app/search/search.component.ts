import { Component, OnInit, Input, ViewChild, ElementRef } from '@angular/core';
import { Router, NavigationExtras, ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.less']
})
export class SearchComponent implements OnInit {
  @ViewChild('inputSearch') private inputSearch: ElementRef;
  @Input() sfHide: boolean;
  timer: number;
  query: string;

  constructor(
    private router: Router,
    private route: ActivatedRoute) { }


  getResults(query: string) {
    if (!query) {
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
      this.query = param['query'];
    });
  }
}
