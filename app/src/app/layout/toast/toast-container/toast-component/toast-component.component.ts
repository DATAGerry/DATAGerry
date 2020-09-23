import {Component, Input, OnInit} from '@angular/core';
import {ToastService} from '../../toast.service';
import {animate, state, style, transition, trigger} from '@angular/animations';

@Component({
  selector: 'cmdb-toast-component',
  templateUrl: './toast-component.component.html',
  styleUrls: ['./toast-component.component.scss'],
})
export class ToastComponentComponent {

  private _toast: any = {};

  @Input()
  public set toast(value: any) {
    this._toast = value;
  }

  public get toast(): any {
    return this._toast;
  }

  constructor(public toastService: ToastService) {
  }

  parse(time: number) {
    if (time) {
      return 'progressBars ' + time.toString() + ' s linear';
    }
    return 'progressBar 5s linear';
  }

  waitTillDisposal(time: number, toast) {
    // tslint:disable-next-line:only-arrow-functions
    console.log(toast);
    function delay(ms: number) {
      return new Promise( resolve => {
        setTimeout(resolve, ms);
      });
    }

    (async () => {
      await delay(time);
      if (toast) {
        this.toastService.remove(toast);
      }
    })();
  }

}
