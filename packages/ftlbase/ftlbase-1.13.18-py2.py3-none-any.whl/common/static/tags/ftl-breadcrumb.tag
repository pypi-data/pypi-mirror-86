<ftl-breadcrumb>
  <div class="ftl-breadcrumb { ftl-breadcrumb-numbered : opts.numbered }">
    <a each="{link, index in opts.links}" href="{link.url}" class="{active : link.active}">{link.text} <span if={link.badge} class="badge">{ link.badge }</span></a>
  </div>

  <script>
    var self = this;

    linkclicked = function (e) {
      sellink = e.item.link;
      link = {
        text: sellink.text,
        url: sellink.url
      };

      self.trigger("link-clicked", link);
    };

    self.on("before-mount", function () {
      // Parâmetros:
      //     links: [{url, text, active, badge }, ] active coloca background black, badge é o texto de um badge anexado
      //     numbered: true / false, se é para mostrar o círculo com o nível do breadcrumb na frente do texto
      // Ver exemplo do gráfico de sunburst onde não se mostra os números
      if (!self.opts.links) self.opts.links = {links: []};
    });
  </script>
</ftl-breadcrumb>