from ..models import*
from ..exceptions import*

class ForfaitServive:

    def save(self, request):
        #   CRE UN NOUVEL ENREGISTREMENT DE FORFAIT

        f=Forfait.objects.create(
            name=request.POST.get('name'),
            duration=int(request.POST.get('duration')),
            price=float(request.POST.get('price')),
        )

        return f.to_json()

    def show(self,id):
        # RENVOIE LE FORFAIT AVEC L'ID AU FORMAT JSON

        try:
            return Forfait.objects.get(id=id).to_json()
        except:
            # FORFAIT INTROUVABLE!
            return ObjectNotFoundException('FORFAIT',id).format()

    def list(self):
        #RENVOIE LA LISTE DES FORFAITS

        return [
            f.to_json() for f in Forfait.objects.all().order_by('-id')
        ]

    def update(self, request,id):
        # MET A JOUR LE FORFAIT AVEC L'ID

        try:
            f=Forfait.objects.get(id=id)
            f.name=request.POST.get('name')
            f.duration=int(request.POST.get('duration'))
            f.price=float(request.POST.get('price'))
            f.save()
        except:
            # FORFAIT INTROUVABLE!
            return ObjectNotFoundException('FORFAIT',id).format()

    def delete(self, id):
        # SUPPRIE LE FORFAIT AVEC L'ID

        try:
            Forfait.objects.get(id=id).delete()
            return {
                'delected': True
            }
        except:
            # FORFAIT INTROUVABLE!
            return ObjectNotFoundException('FORFAIT',id).format()