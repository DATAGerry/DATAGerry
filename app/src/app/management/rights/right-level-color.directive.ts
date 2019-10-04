import { Directive, ElementRef, HostBinding, Input, OnChanges, Renderer2, SimpleChanges } from '@angular/core';

@Directive({
  selector: '[rightLevelColor]'
})
export class RightLevelColorDirective implements OnChanges {

  @Input() classPrefix: string = '';
  @Input() level: number = 0;

  private readonly levelColor = {
    100: 'danger',
    80: 'primary',
    50: 'secondary',
    30: 'info',
    10: 'dark',
    0: ''
  };

  public constructor(private renderer: Renderer2, private hostElement: ElementRef) {

  }

  public ngOnChanges(changes: SimpleChanges): void {
    const addClass = `${ this.classPrefix }${ this.levelColor[this.level] }`;
    if (addClass !== '') {
      this.renderer.addClass(this.hostElement.nativeElement, addClass);
    }
  }

}
