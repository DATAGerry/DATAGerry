import { Component, Input, OnInit } from '@angular/core';
import { LinkService } from '../../../services/link.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbLink } from '../../../models/cmdb-link';

@Component({
  selector: 'cmdb-object-links',
  templateUrl: './object-links.component.html',
  styleUrls: ['./object-links.component.scss']
})
export class ObjectLinksComponent implements OnInit {

  @Input() partnerID: number;
  public linkAddForm: FormGroup;

  constructor(private linkService: LinkService) {
  }

  public ngOnInit(): void {
    this.linkAddForm = new FormGroup({
      secondary: new FormControl(0, Validators.required)
    });
  }

  public addLink() {
    if (this.linkAddForm.valid) {
      const newLink: CmdbLink = new CmdbLink();
      newLink.primary = +this.partnerID;
      newLink.secondary = +this.linkAddForm.get('secondary').value;
      this.linkService.postLink(newLink).subscribe((ack) => {
          console.log(ack);
        },
        (error) => {
          console.error(error);
        },
        () => {

        });
    }
  }
}
