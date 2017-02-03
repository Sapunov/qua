import { Subject } from 'rxjs/Subject';
import { Subscription }   from 'rxjs/Subscription';
import { Component, OnInit, OnDestroy, Input, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { Router, NavigationExtras, ActivatedRoute, Params } from '@angular/router';

import { SearchService } from '../../services/search.service';
import { ISearchInfo } from '../../interfaces/search-hits.interface';

import { MIN_CHARS_FOR_SEARCH, SEARCH_DELAY } from '../../../environments/const';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.less']
})
export class SearchComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild('inputSearch') private searchField: ElementRef;
  @Input() focusOnSf: Subject<boolean>;
  @Input() sfHide: boolean;
  subs: Subscription[];
  query: string;
  timer: number;
  searchInfo: ISearchInfo;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private searchService: SearchService
    ) {
      this.query = '';
      this.subs = [];
      this.searchInfo = null;
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
    }, SEARCH_DELAY);
  }

  ngOnInit() {
    this.subs.push(this.searchService.searchInfo$.subscribe((info) => {
      this.searchInfo = info;
    }));
    this.route.queryParams.subscribe((param: Params) => {
      this.query = param['query'] || '';
    });
  }

  ngAfterViewInit() {
    this.searchField.nativeElement.focus();
    this.subs.push(this.focusOnSf.subscribe((focus: boolean) => {
      this.searchField.nativeElement.focus();
    }));
  }

  ngOnDestroy() {
    this.subs.forEach(sub => sub.unsubscribe());
  }
}
