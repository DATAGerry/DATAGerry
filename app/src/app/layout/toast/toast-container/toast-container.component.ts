import {Component} from '@angular/core';
import {ToastService} from '../toast.service';
import {animate, state, style, transition, trigger} from '@angular/animations';


@Component({
  selector: 'cmdb-toast-container',
  templateUrl: './toast-container.component.html',
  styleUrls: ['./toast-container.component.scss'],
  animations: [
    // the fade-in/fade-out animation.
    trigger('simpleFadeAnimation', [

      state('in', style({opacity: 1})),

      transition(':enter', [
        style({opacity: 0}),
        animate(500 )
      ]),

      transition(':leave',
        animate(500, style({opacity: 0})))
    ])
  ]
})


export class ToastContainerComponent {

  constructor(public toastService: ToastService) {
  }

  parse(time: number) {
    if (time) {
      return 'progressBars ' + time.toString() + ' s linear';
    }
    return 'progressBar 20s linear';
  }

  waitTillDisposal(time: number, toast) {
    // tslint:disable-next-line:only-arrow-functions
    time = 20000;
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
