# Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu) 
Global AI Hub Akbank Python ile Yapay Zekaya Giriş Bootcamp Projesi Açıklaması

**Proje Hakkında**

Bu proje, bir metro ağında **en az aktarma ile** veya **en kısa sürede** bir noktadan diğerine ulaşmayı sağlayan algoritmaları içermektedir. **BFS (Breadth-First Search)** ve *A (A-Star Search)** algoritmaları kullanılarak farklı senaryolara uygun yollar bulunur.

**Projede kullanılan başlıca teknolojiler ve kütüphaneler şunlardır:**

- **Python**: Algoritmaların yazıldığı programlama dili.
- **`heapq`**: A* algoritmasında en düşük maliyetli düğümü bulmak için kullanılan öncelikli kuyruğu yönetir.
- **`collections.deque`**: BFS algoritmasında kullanılan **FIFO (First In First Out)** kuyruk yapısını sağlar.
- **`json`** (opsiyonel): Eğer metro verilerini dış bir dosyadan almak istersek kullanılabilir.
- **`matplotlib.pyplot`**: Metro ağının grafiksel olarak gösterimini sağlamak için kullanılır.
- **`networkx`**: Graf yapısı oluşturmak, düğüm ve bağlantıları görselleştirmek için kullanılır.
- **`numpy`**: Matematiksel hesaplamalar ve diziler için kullanılır.
- **`matplotlib.widgets.Button`**: Kullanıcı arayüzüne buton eklemek ve interaktif grafikler oluşturmak için kullanılır.
- **`sys`**: Komut satırından argüman almayı ve programın çalışma akışını yönetmeyi sağlar.

**Algoritmaların Çalışma Mantığı**

**BFS (Genişlik Öncelikli Arama) Algoritması**

**Çalışma Prensibi:**

- Bir kuyruğa başlangıç düğümünü ekler.
- Her iterasyonda, kuyruğun başındaki düğüm genişletilir ve komşu düğümler kuyruğa eklenir.
- Hedef düğümüne ulaşıldığında en az aktarma ile gidilen rota bulunmuş olur.

**Neden BFS?**

- Eğer **her durak aynı mesafede** kabul edilirse **en kısa aktarmasız yolu** bulmak için uygundur.
- Grafiğin tüm düğümlerini eşit seviyede ziyaret eder, bu yüzden **optimal çözüm garantisi vardır**.

***A (A-Star) Algoritması***

**Çalışma Prensibi:**

- Her durak için **gerçek maliyet (g) + tahmini maliyet (h)** hesaplanarak en iyi yol seçilir.
- **Öncelik kuyruğu (heap)** kullanılarak en düşük toplam maliyetli düğüm genişletilir.
- Daha akıllı arama yaptığı için gereksiz yolları elemiş olur.

**Neden A-star?***

- Eğer **duraklar arasında mesafeler farklıysa**, en hızlı yolu bulmak için uygundur.
- BFS’den daha hızlı çalışabilir çünkü **öncelikli olarak en umut verici yolları genişletir**.

- ![image](https://github.com/user-attachments/assets/42043a30-c7a0-4f2d-91ae-e9e8259403bd)

**Örnek Kullanım ve Test Sonuçları**

***Başlangıç Noktası:** A **Hedef Nokta:** F*

![image](https://github.com/user-attachments/assets/4c1654ad-427c-4673-a10c-403c29f5f6a0)

```python
BFS Path from A to F: ['A', 'D', 'E', 'F']
A* Path from A to F: ['A', 'D', 'E', 'F'], Cost: 13

BFS Path from A to C: ['A', 'B', 'C']
A* Path from A to C: ['A', 'B', 'C'], Cost: 5

BFS Path from B to E: ['B', 'A', 'D', 'E']
A* Path from B to E: ['B', 'A', 'D', 'E'], Cost: 9

BFS Path from A to A: ['A']
A* Path from A to A: ['A'], Cost: 0

BFS Path from X to F: None
```
**BFS Sonucu:**

- **En az aktarma yapılan rota**: `A -> D -> E -> F`

***A* Sonucu:***

- **En kısa süreli rota**: `A -> D -> E -> F`

**Çıkarım:** Eğer bir yolcu **en az aktarma** yapmak isterse **BFS**, **en kısa sürede ulaşmak** isterse **A*** daha uygun olur.

**Gelecekteki Geliştirme Fikirleri**

- **Gerçek metro verileri ile test etmek**: Şehirlerin güncel metro verileri eklenerek gerçekçi senaryolar oluşturulabilir.
- **Arayüz geliştirme**: Kullanıcı dostu bir görsel arayüz eklenerek algoritmaların etkileşimli şekilde çalıştırılması sağlanabilir.
- **Toplu taşıma entegrasyonu**: Otobüs, tramvay gibi farklı ulaşım araçları da dahil edilerek daha kapsamlı bir rota bulma sistemi oluşturulabilir.
A* Path from X to F: None, Cost: inf



