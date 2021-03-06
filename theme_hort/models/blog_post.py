# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016 Trustcode - www.trustcode.com.br                         #
#              Danimar Ribeiro <danimaribeiro@gmail.com>                      #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
###############################################################################


from openerp import api, fields, models
from openerp.addons.website.models.website import slug


class BlogBlog(models.Model):
    _inherit = 'blog.blog'

    def _last_post_image(self):
        for item in self:
            last_post = self.env['blog.post'].search(
                [('blog_id', '=', item.id)], limit=1, order='id desc')
            item.last_post_image = last_post.imagem_thumb

    writer_id = fields.Many2one('res.partner', string="Escritor")
    writer_partner_ids = fields.Many2many(
        comodel_name='res.partner', string="Escritores",
        relation="res_partner_blog_blog_rel_writer",
        help="Parceiros que tem permissão de escrver no blog")

    last_post_image = fields.Binary(compute=_last_post_image, store=False)


class BlogPostCategory(models.Model):
    _name = 'blog.post.category'

    name = fields.Char('Nome', size=50, required=True)


class BlogPost(models.Model):
    _inherit = 'blog.post'

    category_id = fields.Many2one('blog.post.category', string="Categoria")
    imagem_thumb = fields.Binary('Background Image')
    email_sent = fields.Boolean('Email enviado')

    @api.multi
    def url_post(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        link = "%s/blog/%s/post/%s" % (base_url, slug(self.blog_id),
                                       slug(self))
        return link
