# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Infographic'
        db.create_table(u'infographics_infographic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_insert', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm["%s.%s" % (User._meta.app_label, User._meta.object_name)])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site'])),
            ('site_iid', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, max_length=4, null=True, blank=True)),
            ('site_domain', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, null=True, blank=True)),
            ('date_available', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, db_index=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=4000, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('headline', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['channels.Channel'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('top_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='infographic_topimage', null=True, on_delete=models.SET_NULL, to=orm['images.Image'])),
            ('main_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='infographic_image', null=True, on_delete=models.SET_NULL, to=orm['images.Image'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.CharField')(default='gallery', max_length=20)),
            ('css_text', self.gf('django.db.models.fields.TextField')(default='\n    .infographic-box {\n\n    }\n    #infographic-top-image {\n\n    }\n    #infographic-top-image img {\n\n    }\n    #infographic-menu-items {\n        position:relative; top:-42px;\n    }\n    #infographic-menu-items .menu {\n        list-style:none;\n    }\n    #infographic-menu-items .item-menu {\n        float:left;\n        margin-right:10px;\n    }\n    #infographic-menu-items .item-menu a {\n        color: #FFA500;\n    }\n    #infographic-menu-items .item-menu a.item-active {\n       color:#FFFFFF;\n    }\n\n    #infographic-content {\n       clear:both;\n       width:960px;\n    }\n    #infographic-item-description {\n       float:left;\n       max-width:320px;\n       height:400px;\n       width:320px;\n       overflow-y:scroll\n    }\n    #infographic-item-image {\n       float:right;\n       width:600px;\n    }\n    ', null=True, blank=True)),
            ('css_path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('js_path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('timeline', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='infographic_timeline', null=True, on_delete=models.SET_NULL, to=orm['timelinejs.Timeline'])),
        ))
        db.send_create_signal(u'infographics', ['Infographic'])

        # Adding unique constraint on 'Infographic', fields ['site', 'slug']
        db.create_unique(u'infographics_infographic', ['site_id', 'slug'])

        # Adding model 'InfographicInfographicItem'
        db.create_table(u'infographics_infographicinfographicitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='infographicitem_item', null=True, on_delete=models.SET_NULL, to=orm['infographics.InfographicItem'])),
            ('infographic', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='infographicitem_infographic', null=True, on_delete=models.SET_NULL, to=orm['infographics.Infographic'])),
        ))
        db.send_create_signal(u'infographics', ['InfographicInfographicItem'])

        # Adding model 'InfographicContainer'
        db.create_table(u'infographics_infographiccontainer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='infographiccontainer_container', null=True, on_delete=models.SET_NULL, to=orm['containers.Container'])),
            ('infographic', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='infographiccontainer_infographic', null=True, on_delete=models.SET_NULL, to=orm['infographics.Infographic'])),
        ))
        db.send_create_signal(u'infographics', ['InfographicContainer'])

        # Adding model 'InfographicItem'
        db.create_table(u'infographics_infographicitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['images.Image'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='infographicitem_album', null=True, on_delete=models.SET_NULL, to=orm['articles.Album'])),
            ('timeline', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='infographicitem_timeline', null=True, on_delete=models.SET_NULL, to=orm['timelinejs.Timeline'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('css_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'infographics', ['InfographicItem'])


    def backwards(self, orm):
        # Removing unique constraint on 'Infographic', fields ['site', 'slug']
        db.delete_unique(u'infographics_infographic', ['site_id', 'slug'])

        # Deleting model 'Infographic'
        db.delete_table(u'infographics_infographic')

        # Deleting model 'InfographicInfographicItem'
        db.delete_table(u'infographics_infographicinfographicitem')

        # Deleting model 'InfographicContainer'
        db.delete_table(u'infographics_infographiccontainer')

        # Deleting model 'InfographicItem'
        db.delete_table(u'infographics_infographicitem')


    models = {
        u'articles.album': {
            'Meta': {'object_name': 'Album'},
            u'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['containers.Container']", 'unique': 'True', 'primary_key': 'True'}),
            'headline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'channels.channel': {
            'Meta': {'ordering': "['name', 'parent__id', 'published']", 'unique_together': "(('site', 'long_slug', 'slug', 'parent'),)", 'object_name': 'Channel'},
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'homepage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_in_main_rss': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'long_slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subchannel'", 'null': 'True', 'to': u"orm['channels.Channel']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'show_in_menu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'site_domain': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_iid': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'containers.container': {
            'Meta': {'ordering': "['-date_available', 'title', 'channel_long_slug']", 'unique_together': "(('site', 'child_class', 'channel_long_slug', 'slug'),)", 'object_name': 'Container'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['channels.Channel']"}),
            'channel_long_slug': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'channel_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'child_app_label': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'child_class': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'child_module': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'hat': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['images.Image']", 'null': 'True', 'through': u"orm['containers.ContainerImage']", 'blank': 'True'}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'containers_container_mainimage'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['images.Image']"}),
            'main_image_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'show_on_root_channel': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'site_domain': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_iid': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['sources.Source']", 'null': 'True', 'through': u"orm['containers.ContainerSource']", 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'containers.containerimage': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ContainerImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['containers.Container']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['images.Image']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'containers.containersource': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ContainerSource'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['containers.Container']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'containersource_sources'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['sources.Source']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'images.image': {
            'Meta': {'object_name': 'Image'},
            'archive': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'crop_example': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'crop_x1': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'crop_x2': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'crop_y1': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'crop_y2': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fit_in': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'flip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'halign': ('django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'site_domain': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_iid': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'smart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sources.Source']", 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'valign': ('django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '6', 'null': 'True', 'blank': 'True'})
        },
        u'infographics.infographic': {
            'Meta': {'ordering': "['order']", 'unique_together': "(['site', 'slug'],)", 'object_name': 'Infographic'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['channels.Channel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'containers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'infographic_container'", 'to': u"orm['containers.Container']", 'through': u"orm['infographics.InfographicContainer']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'css_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'css_text': ('django.db.models.fields.TextField', [], {'default': "'\\n    .infographic-box {\\n\\n    }\\n    #infographic-top-image {\\n\\n    }\\n    #infographic-top-image img {\\n\\n    }\\n    #infographic-menu-items {\\n        position:relative; top:-42px;\\n    }\\n    #infographic-menu-items .menu {\\n        list-style:none;\\n    }\\n    #infographic-menu-items .item-menu {\\n        float:left;\\n        margin-right:10px;\\n    }\\n    #infographic-menu-items .item-menu a {\\n        color: #FFA500;\\n    }\\n    #infographic-menu-items .item-menu a.item-active {\\n       color:#FFFFFF;\\n    }\\n\\n    #infographic-content {\\n       clear:both;\\n       width:960px;\\n    }\\n    #infographic-item-description {\\n       float:left;\\n       max-width:320px;\\n       height:400px;\\n       width:320px;\\n       overflow-y:scroll\\n    }\\n    #infographic-item-image {\\n       float:right;\\n       width:600px;\\n    }\\n    '", 'null': 'True', 'blank': 'True'}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'infographic_item'", 'to': u"orm['infographics.InfographicItem']", 'through': u"orm['infographics.InfographicInfographicItem']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'js_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'infographic_image'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['images.Image']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'site_domain': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_iid': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'tags': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4000', 'null': 'True', 'blank': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'infographic_timeline'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['timelinejs.Timeline']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'top_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'infographic_topimage'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['images.Image']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'gallery'", 'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'infographics.infographiccontainer': {
            'Meta': {'object_name': 'InfographicContainer'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'infographiccontainer_container'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['containers.Container']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infographic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'infographiccontainer_infographic'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['infographics.Infographic']"})
        },
        u'infographics.infographicinfographicitem': {
            'Meta': {'object_name': 'InfographicInfographicItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infographic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'infographicitem_infographic'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['infographics.Infographic']"}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'infographicitem_item'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['infographics.InfographicItem']"})
        },
        u'infographics.infographicitem': {
            'Meta': {'object_name': 'InfographicItem'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'infographicitem_album'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['articles.Album']"}),
            'css_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['images.Image']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'infographicitem_timeline'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['timelinejs.Timeline']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'sources.source': {
            'Meta': {'unique_together': "(('site', 'slug'),)", 'object_name': 'Source'},
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'site_domain': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_iid': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'timelinejs.timeline': {
            'Meta': {'object_name': 'Timeline'},
            'asset_caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'asset_credit': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'asset_media': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['channels.Channel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'containers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'timeline_container'", 'to': u"orm['containers.Container']", 'through': u"orm['timelinejs.TimelineContainer']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '50'})
        },
        u'timelinejs.timelinecontainer': {
            'Meta': {'object_name': 'TimelineContainer'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'timelinecontainer_container'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['containers.Container']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'timelinecontainer_timeline'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['timelinejs.Timeline']"})
        }
    }

    complete_apps = ['infographics']