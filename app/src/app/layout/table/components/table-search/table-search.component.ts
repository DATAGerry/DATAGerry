import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { debounceTime, takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'table-search',
  templateUrl: './table-search.component.html',
  styleUrls: ['./table-search.component.scss']
})
export class TableSearchComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  public searchFormGroup: FormGroup;

  @Input() public searchDebounceTime: number = 500;
  @Output() public searchChange: EventEmitter<string> = new EventEmitter<string>();

  constructor() {
    this.searchFormGroup = new FormGroup({
      searchInput: new FormControl()
    });
  }

  public ngOnInit(): void {
    this.searchFormGroup.get('searchInput').valueChanges
      .pipe(takeUntil(this.subscriber)).pipe(debounceTime(this.searchDebounceTime))
      .subscribe(change => this.emitChange(change));
  }

  public emitChange(input: string): void {
    this.searchChange.emit(input);
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
