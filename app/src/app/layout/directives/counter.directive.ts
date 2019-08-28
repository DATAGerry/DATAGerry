import { Directive, EventEmitter, Input, OnChanges, OnDestroy, Output } from '@angular/core';
import { Subject, Subscription, timer } from 'rxjs';
import { switchMap, take, tap } from 'rxjs/operators';

@Directive({
  // tslint:disable-next-line:directive-selector
  selector: '[token]'
})
export class CounterDirective implements OnChanges, OnDestroy {

  private counterSource = new Subject<any>();
  private subscription = Subscription.EMPTY;

  @Input() counter: number;
  @Input() interval: number;
  @Output() value = new EventEmitter<number>();

  constructor() {

    this.subscription = this.counterSource.pipe(
      switchMap(({ interval, count }) =>
        timer(0, interval).pipe(
          take(count),
          tap(() => this.value.emit(count--))
        )
      )
    ).subscribe();
  }

  public ngOnChanges() {
    this.counterSource.next({ count: this.counter, interval: this.interval });
  }

  public ngOnDestroy() {
    this.subscription.unsubscribe();
  }


}
