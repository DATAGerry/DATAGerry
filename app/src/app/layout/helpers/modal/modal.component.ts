import { Component, Input } from '@angular/core';

import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';


@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent {

  @Input() title = 'Information';
  @Input() modalMessage = 'Are you sure, you want to delete all selected objects?';
  @Input() buttonDeny = 'Cancel';
  @Input() buttonAccept = 'Accept';

  constructor(public activeModal: NgbActiveModal) {}

}
