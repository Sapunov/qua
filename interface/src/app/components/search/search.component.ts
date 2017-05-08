import { Subject } from 'rxjs/Subject';
import { Subscription }   from 'rxjs/Subscription';
import { Component, OnInit, OnDestroy, Input, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { Router, NavigationExtras, ActivatedRoute, Params } from '@angular/router';

import { SearchService } from '../../services/search.service';
import { ISearchInfo, ISuggest } from '../../interfaces/search-hits.interface';

import { MIN_CHARS_FOR_SEARCH, LIMIT_FOR_SUGGESTS } from '../../../environments/const';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.less']
})
export class SearchComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild('inputSearch') private searchField: ElementRef;
  @Input() focusOnSf: Subject<boolean>;
  @Input() sfHide: boolean;

  suggests: ISuggest[];
  subs: Subscription[];
  query: string;
  lastQuery: string;
  timer: number;
  searchInfo: ISearchInfo;
  currentSuggest: number;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private searchService: SearchService
    ) {
      this.query = '';
      this.lastQuery = '';
      this.subs = [];
      this.searchInfo = null;
      this.suggests = [];
      this.currentSuggest = -1;
    }


  getResults(query: string): void {
    let params: NavigationExtras = {
      queryParams: {
        query: query
      }
    };

    this.suggests = [];
    this.router.navigate(['/search'], params);
  }

  highlightSuggests(suggests: ISuggest[]): ISuggest[] {
    return suggests.map(suggest => {
      suggest.html = suggest.text.replace(suggest.prefix, `<b style="color: #2b2f33">${suggest.prefix}</b>`);
      return suggest;
    });
  }

  getSuggests(query: string): void {
    if (!query) {
      return;
    }

    if (this.lastQuery === query && this.suggests.length !== 0) {
      return;
    };

    this.lastQuery = query;
    this.currentSuggest = -1;
    this.searchService.getSuggests({
      query: query,
      limit: LIMIT_FOR_SUGGESTS
    })
      .then(suggests => this.suggests = this.highlightSuggests(suggests))
      .catch(err => null);
  }

  useSuggest(suggest: ISuggest): void {
    this.query = suggest.text;
    this.suggests = [];
    this.getResults(this.query);
  }

  onMouseenter(index): void {
    this.currentSuggest = index;
  }

  upDownArrowHandler(code): void {
    if (code === 38) {
      this.currentSuggest -= 1;

      if (this.currentSuggest < 0) {
        this.currentSuggest = this.suggests.length - 1
      }
    }

    if (code === 40) {
      this.currentSuggest += 1;

      if (this.currentSuggest > this.suggests.length - 1) {
        this.currentSuggest = 0
      }
    }

    if (code === 40 || code === 38) {
      this.query = this.suggests[this.currentSuggest].text;
    }
  }

  isSelected(index: number): boolean {
    return index === this.currentSuggest;
  }

  clearSuggests(event): void {
    if (event.target.nodeName === 'LI' || event.target.nodeName === 'INPUT') {
      return;
    } else {
      this.suggests = [];
    }
  }

  keyup(event: KeyboardEvent): void {
    if (
      event.keyCode === 37 ||
      event.keyCode === 38 ||
      event.keyCode === 39 ||
      event.keyCode === 40 ||
      event.keyCode === 13
    ) {
      this.upDownArrowHandler(event.keyCode);
      return;
    }

    if (this.query.length < MIN_CHARS_FOR_SEARCH) {
      this.suggests = [];
      return;
    }

    this.getSuggests(this.query);
  }

  ngOnInit() {
    this.subs.push(this.searchService.searchInfo$.subscribe((info) => {
      this.searchInfo = info;
    }));
    this.route.queryParams.subscribe((param: Params) => {
      let query = param['query'] || '';
      this.query = query.replace(/\+(?=\w|\d|[а-яёА-ЯЁ])/ig, ' ');
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
